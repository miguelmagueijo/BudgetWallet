<script lang="ts">
	import Icon from "@iconify/svelte";
	import WalletCard, { type CardWalletData } from "./WalletCard.svelte";
	import Modal from "$lib/components/Modal.svelte";
	import IconWrapper from "$lib/components/IconWrapper.svelte";
	import { onMount } from "svelte";
	import { DataStore } from "$lib/data.svelte";
	import type { ChangeEventHandler } from "svelte/elements";
	import type { PageProps } from "./$types";

	const { data }: PageProps = $props();

	const DEFAULT_WALLET_ICON = "streamline-ultimate:money-wallet-open-bold";
	const DEFAULT_WALLET_COLOR = "#FFFFFF";
	const STORAGE_WALLET_SORT_KEY = "home:wallet-sort";

	let walletStore: DataStore<CardWalletData> = new DataStore<CardWalletData>(true);
	let walletsSortValue: string | null = $state(null);
	let showAddWalletModal = $state(false);
	let allAccountsMoneyParts: number[] = $state([0, 0]);

	function fetchWallets(ignoreFlag = false) {
		if (!ignoreFlag && walletStore.loading) {
			return;
		}

		walletStore.loading = true;

		fetch("/api/wallets/", {
			credentials: "include",
		})
			.then((res) => {
				if (!res.ok) {
					throw new Error(`HTTP error ${res.status}`);
				}

				return res.json();
			})
			.then((data: CardWalletData[]) => {
				walletStore.setData(data);

				let totalMoney: number = 0;

				for (const w of data) {
					totalMoney += w.total_money;
				}

				allAccountsMoneyParts = totalMoney.toFixed(2).toString().split(".").map(Number);
			})
			.catch((err) => {
				console.error(err);
			})
			.finally(() => {
				walletStore.loading = false;
			});
	}

	const handleFilterWalletOnChange: ChangeEventHandler<HTMLInputElement> = (event) => {
		const value = event.currentTarget.value;

		if (!value) {
			walletStore.resetFilter();
		} else {
			walletStore.applyFilter((element) => element.name.toLowerCase().includes(value.toLowerCase()));
		}
	};

	const sortFunctions: Record<string, (a: CardWalletData, b: CardWalletData) => number> = {
		name: (a, b) => a.name.localeCompare(b.name),
		"name-desc": (a, b) => b.name.localeCompare(a.name),
		balance: (a, b) => a.total_money - b.total_money,
		"balance-desc": (a, b) => b.total_money - a.total_money,
	};

	function handleSortWalletChange() {
		if (!walletsSortValue) {
			return;
		}

		localStorage.setItem(STORAGE_WALLET_SORT_KEY, walletsSortValue);

		return walletStore.applySort(sortFunctions[walletsSortValue] ?? sortFunctions["name"]);
	}

	let newWalletColor = $state(DEFAULT_WALLET_COLOR);
	let newWalletIcon = $state(DEFAULT_WALLET_ICON);
	let newWalletDescription = $state("");
	let newWalletName = $state("");
	let newWalletMoney = $state(0);

	async function handleNewWalletFormSubmit(evt: SubmitEvent) {
		const formData = new FormData(evt.target as HTMLFormElement);

		try {
			const result = await fetch("http://localhost:5173/api/wallets/new", {
				credentials: "include",
				method: "POST",
				body: formData,
			});

			if (!result.ok) {
				throw new Error("Response was not successful");
			}

			const data = await result.json();

			const newWallet: CardWalletData = {
				id: data.id,
				name: newWalletName,
				budgets: [
					{
						id: data.budget_id,
						name: "Money",
						total: newWalletMoney,
					},
				],
				icon: newWalletIcon,
				color: newWalletColor,
				total_money: newWalletMoney,
			};

			walletStore.addRecord(newWallet);

			showAddWalletModal = false;
		} catch (e) {
			console.error(e);
		}
	}

	onMount(async () => {
		walletsSortValue = localStorage.getItem(STORAGE_WALLET_SORT_KEY);
		if (!walletsSortValue) {
			walletsSortValue = "name";
		}

		handleSortWalletChange(); // add sort before fetching data
		fetchWallets(true);
	});
</script>

<Modal bind:showModal={showAddWalletModal} title="New wallet">
	<form id="new-wallet-form" class="max-w-125 space-y-2" onsubmit={handleNewWalletFormSubmit}>
		<div>
			<label class="block font-semibold" for="wallet-name"> Name <span class="text-red-500">*</span> </label>
			<input
				id="wallet-name"
				name="name"
				type="text"
				class="w-full rounded-lg border-2 border-primary-900 bg-black"
				bind:value={newWalletName}
				required
			/>
			<small class="opacity-50"> Min 3 characters </small>
		</div>
		<div>
			<label class="block font-semibold" for="wallet-desc"> Start balance <span class="text-red-500">*</span> </label>
			<input
				id="wallet-money"
				name="start_balance"
				class="w-full rounded-lg border-2 border-primary-900 bg-black"
				type="number"
				bind:value={newWalletMoney}
				required
			/>
		</div>
		<div>
			<label class="block font-semibold" for="wallet-desc"> Description </label>
			<textarea
				id="wallet-desc"
				name="description"
				class="max-h-50 w-full rounded-lg border-2 border-primary-900 bg-black"
				maxlength="512"
				bind:value={newWalletDescription}
			></textarea>
			<small class="flex justify-between opacity-50">
				<span>Max 512</span>
				<span>Total: {newWalletDescription.length}</span>
			</small>
		</div>
		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
				<div>
					<label class="block font-semibold" for="wallet-color"> Icon color </label>
					<input
						id="wallet-color"
						name="color"
						type="color"
						class="h-11 w-full rounded-lg border-2 border-primary-900 bg-black"
						bind:value={newWalletColor}
					/>
				</div>
				<div class="mt-2">
					<label class="block font-semibold" for="wallet-color"> Icon </label>
					<input
						id="wallet-color"
						name="iconify_name"
						type="text"
						class="w-full rounded-lg border-2 border-primary-900 bg-black"
						bind:value={newWalletIcon}
					/>
					<small class="opacity-50">
						Icon name must be from: <a class="font-bold underline" href="https://icon-sets.iconify.design/" target="_blank">Iconify</a>
					</small>
				</div>
			</div>
			<div
				class="flex h-full items-center justify-center rounded-lg border-2 bg-black"
				style="border-color: {newWalletColor}; color: {newWalletColor};"
			>
				<IconWrapper icon={newWalletIcon} classes="size-18">
					{#snippet fallback()}
						<Icon icon={DEFAULT_WALLET_ICON} class="size-18" />
					{/snippet}
				</IconWrapper>
			</div>
		</div>
	</form>
	{#snippet footer()}
		<div class="flex justify-end gap-4">
			<button type="submit" form="new-wallet-form" class="primary-button px-4 py-2"> Create wallet </button>
			<button class="primary-button-outline px-4 py-2" type="button" onclick={() => (showAddWalletModal = false)}> Cancel </button>
		</div>
	{/snippet}
</Modal>

<section class="my-10">
	<h2 class="mb-4 text-5xl font-bold">Hi, <span class="capitalize">{data.user.username}</span></h2>
	<div class="grid grid-cols-3 gap-8">
		<div class="info-card border-primary-400 bg-primary-925 text-primary-400">
			<Icon icon="ph:money-wavy" class="size-18" />
			<div class="text-right text-4xl font-bold text-primary-50">
				{#if walletStore.loading}
					-- <span class="text-lg font-semibold">€</span>
				{:else}
					{allAccountsMoneyParts[0]}<span class="text-lg font-semibold"
						>{allAccountsMoneyParts[1] === 0 ? "" : "." + allAccountsMoneyParts[1]} €</span
					>
				{/if}
			</div>

			<div class="info-card-tooltip">
				<span class="bg-primary-400 text-primary-950 after:border-b-primary-400"> Your total balance </span>
			</div>
		</div>
		<div class="relative flex items-center justify-between rounded-lg bg-primary-400 p-4 text-primary-950">
			<Icon icon="mingcute:stock-line" class="size-18" />
			<div class="text-right text-4xl font-bold">912<span class="text-lg font-semibold">.73€</span></div>
			<div class="absolute top-0 right-0 bottom-0 left-0 z-90 flex items-center bg-black/90 text-white">
				<div class="w-full text-center text-2xl font-bold text-primary-200">Coming soon...</div>
			</div>
		</div>
		<div class="relative flex items-center justify-between rounded-lg bg-primary-400 p-4 text-primary-950">
			<Icon icon="fluent:money-calculator-20-regular" class="size-18" />
			<div class="text-right text-4xl font-bold">0.10<span class="text-lg font-semibold">€/day</span></div>
			<div class="absolute top-0 right-0 bottom-0 left-0 z-90 flex items-center bg-black/90 text-white">
				<div class="w-full text-center text-2xl font-bold text-primary-200">Coming soon...</div>
			</div>
		</div>
	</div>
</section>

<section>
	<div class="flex items-end gap-2">
		<h2 class="text-4xl font-bold">Your wallets</h2>
		<span class="opacity-50">({walletStore.loading ? "-" : walletStore.getSize()}/10)</span>
	</div>
	<div class="my-4">
		<form class="flex items-center gap-4">
			<button
				type="button"
				class="group cursor-pointer rounded-lg border-2 border-primary-700 bg-black p-3 disabled:pointer-events-none disabled:opacity-25"
				onclick={() => fetchWallets()}
				disabled={walletStore.loading}
			>
				<Icon icon="tabler:refresh" class="size-6 duration-300 group-hover:-rotate-180" />
			</button>
			<div class="flex w-fit items-center rounded-lg border-2 border-primary-700 bg-black p-1 px-2">
				<Icon icon="ic:baseline-search" class="size-6 text-primary-700" />
				<input
					type="text"
					class="w-100 rounded-lg border-0 bg-transparent text-white focus:ring-0"
					onchange={handleFilterWalletOnChange}
					placeholder="Filter by name"
				/>
			</div>
			<div>
				<select
					class="w-fit rounded-lg border-2 border-primary-700 bg-black p-3 pr-10 font-semibold text-green-100"
					bind:value={walletsSortValue}
					onchange={handleSortWalletChange}
				>
					<!-- TODO: implement favorites -->
					<!-- <option>Favorites</option> -->
					<option value="name">A-Z</option>
					<option value="name-desc">Z-A</option>
					<option value="balance">Balance (Asc.)</option>
					<option value="balance-desc">Balance (Desc.)</option>
				</select>
			</div>
		</form>
	</div>
	<div class="mt-6 grid grid-cols-1 gap-8 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
		{#if walletStore.loading}
			{#each [1, 2, 3, 4] as i (i)}
				<WalletCard id={-i} title="" iconName="" color="" budgets={[]} totalMoney={-1} />
			{/each}
		{:else if walletStore.isEmpty()}
			<div
				class="col-span-4 flex w-full flex-col items-center justify-center gap-y-2 rounded-lg border-3 border-primary-900 bg-primary-950 py-6 text-primary-100"
			>
				<Icon icon="simple-line-icons:drawer" class="size-12 stroke-2" />
				<p class="text-center text-xl font-bold">You don't have any wallets</p>
			</div>
		{:else if walletStore.isOutEmpty()}
			<div
				class="col-span-4 flex w-full flex-col items-center justify-center gap-y-2 rounded-lg border-3 border-primary-900 bg-primary-950 py-6 text-primary-100"
			>
				<Icon icon="lucide:search-x" class="size-12 stroke-2" />
				<p class="text-center text-xl font-bold">No wallets were found for your search</p>
			</div>
		{:else}
			{#each walletStore.dataOut as wallet (wallet.id)}
				<WalletCard
					id={wallet.id}
					title={wallet.name}
					iconName={wallet.icon ?? DEFAULT_WALLET_ICON}
					color={wallet.color ?? DEFAULT_WALLET_COLOR}
					budgets={wallet.budgets}
					totalMoney={wallet.total_money}
				/>
			{/each}
		{/if}
	</div>
	<div class="mt-4">
		<button
			type="button"
			class="primary-button-outline flex w-full items-center justify-center gap-1 py-5"
			onclick={() => {
				showAddWalletModal = true;
				newWalletName = "";
				newWalletDescription = "";
				newWalletMoney = 0;
				newWalletColor = DEFAULT_WALLET_COLOR;
				newWalletIcon = DEFAULT_WALLET_ICON;
			}}
		>
			<span>Create new wallet</span>
			<Icon icon="typcn:plus" class="size-5" />
		</button>
	</div>
</section>

<style lang="postcss">
	@reference "tailwindcss";

	.info-card {
		@apply rounded-lg border-2 p-4;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.info-card-tooltip {
		position: absolute;
		left: 50%;
		top: 100%;
		visibility: hidden;
		transform: translateX(-50%);
	}

	.info-card-tooltip > span {
		@apply mt-4 rounded-lg border-2 px-4 py-2 font-semibold;
		display: block;
		text-align: center;
		border-color: transparent;
		width: fit-content;
	}

	.info-card-tooltip > span::after {
		content: "";
		position: absolute;
		top: -3px;
		left: 50%;
		transform: translateX(-50%);
		border-width: 10px;
		border-style: solid;
		border-left-color: transparent;
		border-right-color: transparent;
		border-top-color: transparent;
	}

	.info-card:hover .info-card-tooltip {
		visibility: visible;
	}
</style>
