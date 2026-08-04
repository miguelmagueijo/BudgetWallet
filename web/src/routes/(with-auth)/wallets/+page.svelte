<script lang="ts">
	import Icon from "@iconify/svelte";
	import { DataStore } from "$lib/data.svelte";
	import { onMount } from "svelte";
	import { getTextColorForHexBg } from "$lib/colorsUtils";
	import { ICONS_NAMES } from "$lib";
	import Drawer from "$lib/components/Drawer.svelte";

	interface IMovementCategory {
		id: number;
		title: string;
		color?: string;
		is_global: boolean;
	}

	interface IMovement {
		id: number;
		title: string;
		amount: string;
		is_deposit: boolean;
		done_at: string;
		category?: IMovementCategory;
	}

	interface IBudget {
		id: number;
		name: string;
		balance: string; // it's decimal string!
	}

	interface IWallet {
		id: number;
		name: string;
		icon?: string;
		color?: string;
		balance: string; // it's decimal string!
		budgets?: Array<IBudget>;
	}

	interface BudgetDetailsInfo {
		walletColor?: string;
		walletName: string;
		budgetId: number;
		budgetName: string;
		budgetBalance: number;
	}

	interface WalletDrawerData {
		isOpen: boolean;
		editId: number | null;
		name: string;
		icon?: string;
		color?: string;
	}

	const walletsStore: DataStore<IWallet> = new DataStore<IWallet>("/api/wallets/?with_budgets=true");

	let movementsStore: DataStore<IMovement> | null = $state(null);
	let budgetDetailsInfo: BudgetDetailsInfo | null = $state(null);
	let showBudgetDetails = $state(false);

	onMount(() => {
		walletsStore.load();
	});

	function openBudgetDetailsDrawer(wallet: IWallet, budget: IBudget) {
		showBudgetDetails = true;

		if (budgetDetailsInfo && budgetDetailsInfo.budgetId === budget.id) {
			return;
		}

		budgetDetailsInfo = {
			walletColor: wallet.color,
			walletName: wallet.name,
			budgetId: budget.id,
			budgetName: budget.name,
			budgetBalance: Number(Number(budget.balance).toFixed(2)),
		};
		movementsStore = new DataStore(`/api/budgets/${budget.id}/movements`, true);
	}

	function closeBudgetDetailsDrawer() {
		showBudgetDetails = false;
	}

	const walletDrawerData: WalletDrawerData = $state({
		isOpen: false,
		editId: null,
		name: "",
		icon: "",
		color: "#FFFFFF"
	});

	function openWalletDrawer(walletToEdit?: IWallet) {
		if (!walletToEdit) {
			walletDrawerData.editId = null;
			walletDrawerData.name = "";
			walletDrawerData.icon = "";
			walletDrawerData.color = "#FFFFFF";
		} else {
			walletDrawerData.editId = walletToEdit.id;
			walletDrawerData.name = walletToEdit.name;
			walletDrawerData.icon = walletToEdit.icon;
			walletDrawerData.color = walletToEdit.color ?? "#FFFFFF";
		}

		walletDrawerData.isOpen = true;
	}
</script>

<svelte:head>
	<title>BW | Wallets</title>
</svelte:head>

<Drawer bind:showDrawer={walletDrawerData.isOpen}>
	{#snippet header()}
		<div class="flex items-center justify-between">
			<h2 class="text-xl font-bold">
				{#if walletDrawerData.editId === null}
					New wallet
				{:else}
					Edit wallet
				{/if}
			</h2>
			<button class="cursor-pointer text-gray-600" onclick={() => (walletDrawerData.isOpen = false)}>
				<Icon icon={ICONS_NAMES.x} class="size-5" />
			</button>
		</div>
		<p class="mt-2 text-gray-500">
			{#if walletDrawerData.editId === null}
				Create a new tracking of your money
			{:else}
				Let's update the details
			{/if}
		</p>
	{/snippet}
	<form>
		<label class="block font-semibold">
			Name <span class="text-red-500">*</span>
			<input type="text" class="mt-2 w-full rounded-lg border-2 border-primary-800 bg-primary-1000" bind:value={walletDrawerData.name} />
		</label>
		<label class="mt-6 block font-semibold">
			Color
			<input type="color" class="mt-2 h-11 w-full rounded-lg border-2 border-transparent" bind:value={walletDrawerData.color} />
			<small class="text-xs text-gray-500">Defaults to white</small>
		</label>
		<div class="mt-6 items-center justify-between gap-4 {walletDrawerData.icon ? 'grid grid-cols-[1fr_auto]' : ''}">
			<label class="block font-semibold">
				Icon
				<input type="text" class="mt-2 h-11 w-full rounded-lg border-2 border-primary-800 bg-primary-1000" bind:value={walletDrawerData.icon} />
				<small class="text-xs text-gray-500">
					<a class="mt-2 flex items-center gap-1 underline" href="https://icon-sets.iconify.design/" target="_blank">
						<span>Open icons catalog</span>
						<Icon icon="lucide:external-link" />
					</a>
				</small>
			</label>
			{#if walletDrawerData.icon}
				<div
					class="flex size-18 items-center justify-center rounded-lg border-2 border-primary-800 p-3"
					style:color={walletDrawerData.color}
					style:border-color={walletDrawerData.color}
				>
					<Icon icon={walletDrawerData.icon} class="size-full stroke-2" />
				</div>
			{/if}
		</div>
	</form>
	{#snippet footer()}
		<div class="flex gap-2">
			<button
				class="w-26 cursor-pointer rounded-lg border-2 border-transparent bg-primary-600 py-2 font-semibold text-primary-0 duration-200 hover:bg-primary-800"
				onclick={() => (walletDrawerData.isOpen = false)}
			>
				{#if walletDrawerData.editId === null}
					Create
				{:else}
					Update
				{/if}
			</button>
			<button
				class="w-26 cursor-pointer rounded-lg border-2 border-transparent py-2 font-semibold duration-200 hover:bg-gray-800"
				onclick={() => (walletDrawerData.isOpen = false)}
			>
				Cancel
			</button>
		</div>
	{/snippet}
</Drawer>

<div class="fixed inset-0 top-0 right-0 bottom-0 left-0 z-50 duration-200" class:opacity-0={!showBudgetDetails} class:invisible={!showBudgetDetails}>
	<div class="flex">
		<button onclick={closeBudgetDetailsDrawer} title="" class="block h-screen flex-1 bg-black/75"></button>
		<div
			class="absolute top-0 right-0 bottom-0 flex min-w-1/2 flex-col bg-primary-950 transition-all duration-200"
			class:translate-x-full={!showBudgetDetails}
			class:translate-x-0={showBudgetDetails}
		>
			<div class="h-3" style:background-color={budgetDetailsInfo?.walletColor}></div>
			<div class="p-4">
				<div class="text-2xl font-semibold" style:color={budgetDetailsInfo?.walletColor}>
					{budgetDetailsInfo?.walletName}
				</div>
				<div class="mt-4 flex justify-between">
					<div>
						<div class="text-xs opacity-50">Budget</div>
						<div class="text-xl font-bold">{budgetDetailsInfo?.budgetName}</div>
					</div>
					<div>
						<div class="text-right text-xs opacity-50">Balance</div>
						<div>
							<b class="text-xl" class:text-primary-500={(budgetDetailsInfo?.budgetBalance ?? 0) > 0}>
								{budgetDetailsInfo?.budgetBalance}
							</b>
							<small>€</small>
						</div>
					</div>
				</div>
				<div class="mt-2">
					<div class="text-xs opacity-50">Description</div>
					<div>Money available to spend with phone/card</div>
				</div>
				<hr class="mt-4" />
				<div class="mt-6">
					<div class="flex flex-col gap-y-2 rounded-lg bg-primary-1000 p-4">
						<div class="font-bold">Movements</div>
						{#if movementsStore}
							{#if movementsStore.loading}
								{#each [1, 2] as i (i)}
									<div class="rounded-lg border-2 border-primary-0/15 p-3 animate-pulse">
										<div class="h-3 bg-primary-0/15 rounded-lg mb-2"></div>
										<div class="h-5 bg-primary-0/15 rounded-lg"></div>
									</div>
								{/each}
							{:else}
								{#each movementsStore.dataOut as movement (movement.id)}
									{@const realAmount = Number(Number(movement.amount).toFixed(2)) * (movement.is_deposit ? 1 : -1)}
									{@const realDoneDate = new Date(movement.done_at).toLocaleDateString("pt-PT", { hour: "2-digit", minute: "2-digit" })}
									<div class="rounded-lg border-2 border-primary-0/15 p-3">
										<div class="flex items-center justify-between">
											<div class="text-sm opacity-50">
												{realDoneDate}
											</div>
											{#if movement.category}
												<div
													class="w-fit rounded-full px-4 text-xs font-semibold"
													style:background-color={movement.category.color}
													style:color={getTextColorForHexBg(movement.category.color)}
												>
													{movement.category.title}
												</div>
											{/if}
										</div>
										<div class="flex items-center justify-between">
											<div>
												{movement.title}
											</div>
											<div class="font-bold" class:text-primary-500={movement.is_deposit} class:text-red-500={!movement.is_deposit}>
												<b>{realAmount}</b> <small>€</small>
											</div>
										</div>
									</div>
								{:else}
									<p class="text-gray-500">
										No movements yet registered
									</p>
								{/each}
							{/if}
						{:else}
							Something went wrong!
						{/if}
					</div>
				</div>
			</div>
			<div class="flex flex-1 items-end justify-start">
				<div class="w-full bg-primary-1000 px-4 py-6">
					<button
						class="cursor-pointer rounded-lg border-2 border-primary-800/50 px-6 py-2 text-primary-0 duration-200 hover:bg-primary-0/10"
						onclick={closeBudgetDetailsDrawer}
					>
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
</div>

<section>
	<a href="/home" class="mb-4 flex w-fit items-center gap-2 underline opacity-50">
		<Icon icon="pajamas:go-back" />
		<span>Home</span>
	</a>
	<h1 class="text-5xl font-bold">My wallets</h1>
	<div class="mt-12">
		<button
			class="flex cursor-pointer items-center gap-2 rounded-lg bg-primary-600 px-4 py-2 font-semibold"
			onclick={() => openWalletDrawer()}
		>
			<Icon icon={ICONS_NAMES.plus} class="size-4" />
			New wallet
		</button>
	</div>
	{#if walletsStore.loading}
		<div class="mt-12">
			{#each [1, 2, 3] as i (i)}
				<div class="animate-pulse rounded-lg border-2 border-primary-900 bg-primary-950 p-4">
					<div class="flex">
						<div class="flex flex-1 items-center gap-2">
							<div class="size-8 rounded-lg bg-primary-1000"></div>
							<div class="h-8 w-1/2 rounded-lg bg-primary-1000"></div>
						</div>
						<div class="h-8 w-32 bg-primary-1000"></div>
					</div>
					<div class="mt-4 mb-2 h-5 w-16 rounded-lg bg-primary-1000"></div>
					<div class="h-12 w-full rounded-lg bg-primary-1000"></div>
				</div>
			{/each}
		</div>
	{:else}
		<div class="mt-12 flex flex-col gap-6">
			{#each walletsStore.dataOut as wallet (wallet.id)}
				{@const walletBalance = Number(Number(wallet.balance).toFixed(2))}
				<div class="rounded-lg border-2 border-primary-0/25 bg-primary-950 p-4 group" style:border-color={wallet.color}>
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-2" style:color={wallet.color}>
							{#if wallet.icon}
								<Icon icon={wallet.icon} class="size-8 stroke-2" />
							{/if}
							<h2 class="text-xl font-bold">
								{wallet.name}
							</h2>
							<button class="p-1 rounded-lg border-2 border-primary-0/50 text-primary-0/50 hover:bg-primary-700 duration-300 cursor-pointer hover:border-primary-0 hover:text-primary-0 hidden group-hover:block" onclick={() => openWalletDrawer(wallet)}>
								<Icon icon={ICONS_NAMES.edit}/>
							</button>
						</div>
						<div class="text-xl">
							<b class:text-primary-500={walletBalance > 0}>{walletBalance}</b> <span class="text-sm">€</span>
						</div>
					</div>
					<div class="mt-4 mb-2 text-sm opacity-35">Budgets</div>
					<div class="flex flex-col gap-y-2">
						{#if wallet.budgets}
							{#each wallet.budgets as budget (budget.id)}
								{@const budgetBalance = Number(Number(budget.balance).toFixed(2))}
								<button
									class="flex cursor-pointer justify-between rounded-lg border-2 border-primary-0/25 bg-primary-1000 p-4 duration-200 hover:bg-primary-0/10"
									onclick={() => openBudgetDetailsDrawer(wallet, budget)}
								>
									<span class="font-bold">
										{budget.name}
									</span>
									<span>
										<b class:text-primary-500={budgetBalance > 0}>{budgetBalance}</b> <small>€</small>
									</span>
								</button>
							{:else}
								<div class="p-4 bg-primary-1000 rounded-lg text-primary-0/35">No budgets</div>
							{/each}
						{:else}
							<div class="p-4 bg-primary-1000 rounded-lg text-red-500">Erro fetching budgets</div>
						{/if}
					</div>
				</div>
			{:else}
				<div>You don't have any wallets yet. Create one!</div>
			{/each}
		</div>
	{/if}
</section>
