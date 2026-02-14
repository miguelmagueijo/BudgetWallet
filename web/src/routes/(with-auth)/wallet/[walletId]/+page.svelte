<script lang="ts">
	import { resolve } from "$app/paths";
	import Icon from "@iconify/svelte";
	import { DataStore } from "$lib/data.svelte";
	import { getContext, onMount } from "svelte";
	import { ICONS_NAMES } from "$lib";
	import type { ChangeEventHandler } from "svelte/elements";
	import Modal from "$lib/components/Modal.svelte";
	import IconWrapper from "$lib/components/IconWrapper.svelte";
	import { z } from "zod";
	import { BUDGET_NAME_REGEX, HEX_COLOR_REGEX, ICONIFY_ICON_REGEX } from "$lib/forms.svelte";
	import RequirementsOfField from "$lib/components/forms/RequirementsOfField.svelte";
	import { TOAST_TYPE, ToastStore } from "$lib/toast.svelte";

	interface IBudgetSimpleInfo {
		id: string;
		name: string;
		iconify_name: string;
		color: string;
		is_permanent: boolean;
		budget_total: number;
	}

	interface IMovementInfo {
		id: string;
		title: string;
		is_deposit: boolean;
		is_manual: boolean;
		done_at: string;
		color: string;
		amount: number;
		budget_id: number;
		budget_name: number;
		budget_balance: number;
		created_at: string;
		updated_at: string;
	}

	const { data } = $props();
	const toastStore = getContext("toastStore") as ToastStore;

	let showBudgetModal = $state(false);
	let showMovementModal = $state(false);

	let budgetsStore = new DataStore<IBudgetSimpleInfo>(true);
	let movementsStore = new DataStore<IMovementInfo>(true);

	function fetchBudgets(ignoreLoadingFlag: boolean = false) {
		if (!ignoreLoadingFlag && budgetsStore.loading) {
			return;
		}

		budgetsStore.loading = true;

		fetch(`/api/wallets/${data.wallet.id}/budgets`, {
			credentials: "include",
		})
			.then(async (res) => {
				return [!res.ok, await res.json()];
			})
			.then(([isError, budgets]) => {
				if (isError) {
					console.log(budgets.detail);
				} else {
					budgetsStore.setData(budgets);
				}
			})
			.catch((err) => {
				console.log(err);
			})
			.finally(() => {
				budgetsStore.loading = false;
			});
	}

	function fetchMovements(ignoreLoadingFlag: boolean = false) {
		if (!ignoreLoadingFlag && budgetsStore.loading) {
			return;
		}

		movementsStore.loading = true;

		fetch(`/api/wallets/${data.wallet.id}/movements`, {
			credentials: "include",
		})
			.then(async (res) => {
				return [!res.ok, await res.json()];
			})
			.then(([isError, movements]) => {
				if (isError) {
					console.log(movements.detail);
				} else {
					movementsStore.setData(movements);
				}
			})
			.catch((err) => {
				console.log(err);
			})
			.finally(() => {
				movementsStore.loading = false;
			});
	}

	const handleFilterBudgetNameOnChange: ChangeEventHandler<HTMLInputElement> = (event) => {
		const value = event.currentTarget.value;

		if (!value) {
			budgetsStore.resetFilter();
		} else {
			budgetsStore.applyFilter((element) => element.name.toLowerCase().includes(value.toLowerCase()));
		}
	};

	let modalBudgetName = $state("");
	let modalBudgetDesc = $state("");
	let modalBudgetBalance = $state(0);
	let modalBudgetIcon = $state(ICONS_NAMES.pigBank);
	let modalBudgetColor = $state("#FFFFFF");
	const ModalBudgetValidator = z.object({
		name: z.string().regex(BUDGET_NAME_REGEX, "Budget name doesn't meet the requirements"),
		description: z.string().nullish(),
		start_balance: z.number(),
		iconify_name: z.string().regex(ICONIFY_ICON_REGEX, "Budget iconify name is not valid").or(z.literal("")),
		color: z.string().regex(HEX_COLOR_REGEX, "Invalid color hexadecimal value").or(z.literal("")),
	});

	function openNewBudgetModal() {
		modalBudgetName = "";
		modalBudgetDesc = "";
		modalBudgetBalance = 0;
		modalBudgetColor = "#FFFFFF";
		modalBudgetIcon = ICONS_NAMES.pigBank;
		showBudgetModal = true;
	}

	function handleBudgetFormSubmit(evt: SubmitEvent) {
		evt.preventDefault();

		const data = {
			name: modalBudgetName,
			description: modalBudgetDesc,
			start_balance: modalBudgetBalance,
			iconify_name: modalBudgetIcon,
			color: modalBudgetColor,
		};

		const validation = ModalBudgetValidator.safeParse(data);
		if (!validation.success) {
			for (const iss of validation.error.issues) {
				toastStore.push({
					type: TOAST_TYPE.ERROR,
					message: iss.message,
				});
			}
			return;
		}

		const formData = new FormData();
		for (const [key, value] of Object.entries(data)) {
			const valueAsString = String(value);
			if (valueAsString) {
				formData.append(key, valueAsString);
			}
		}

		console.log(formData);
	}

	onMount(() => {
		fetchBudgets(true);
		fetchMovements(true);
	});
</script>

<svelte:head>
	<title>BW | {data.wallet.name}</title>
</svelte:head>

<a href={resolve("/home")} class="flex w-fit items-center gap-1 border-b text-lg">
	<Icon icon="lets-icons:back" />
	<span> Home </span>
</a>

<Modal bind:showModal={showBudgetModal} title="New budget">
	<form id="new-wallet-form" class="max-w-125 space-y-2" onsubmit={handleBudgetFormSubmit}>
		<div>
			<label class="block font-semibold" for="budget-name"> Name <span class="text-red-500">*</span> </label>
			<input
				id="budget-name"
				name="name"
				type="text"
				class="w-full rounded-lg border-2 border-primary-900 bg-black"
				bind:value={modalBudgetName}
				required
			/>
			<RequirementsOfField requirements={["Length between 3 and 32", "Start with a letter or number", "Cannot end with white space"]} />
		</div>
		<div>
			<label class="block font-semibold" for="budget-balance"> Start balance <span class="text-red-500">*</span> </label>
			<input
				id="budget-balance"
				name="start_balance"
				class="w-full rounded-lg border-2 border-primary-900 bg-black"
				type="number"
				bind:value={modalBudgetBalance}
				required
			/>
		</div>
		<div>
			<label class="block font-semibold" for="budget-desc"> Description </label>
			<textarea
				id="budget-desc"
				name="description"
				class="max-h-50 w-full resize-y rounded-lg border-2 border-primary-900 bg-black"
				maxlength="512"
				bind:value={modalBudgetDesc}
			></textarea>
			<small class="flex justify-end opacity-50">
				<span>{modalBudgetDesc.length}/512</span>
			</small>
		</div>
		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
				<div>
					<label class="block font-semibold" for="budget-color"> Icon color </label>
					<input
						id="budget-color"
						name="color"
						type="color"
						class="h-11 w-full rounded-lg border-2 border-primary-900 bg-black"
						bind:value={modalBudgetColor}
					/>
				</div>
				<div class="mt-2">
					<label class="block font-semibold" for="budget-color"> Icon </label>
					<input
						id="budget-color"
						name="iconify_name"
						type="text"
						class="w-full rounded-lg border-2 border-primary-900 bg-black"
						bind:value={modalBudgetIcon}
					/>
					<small class="opacity-50">
						Icon name must be from: <a class="font-bold underline" href="https://icon-sets.iconify.design/" target="_blank">Iconify</a>
					</small>
				</div>
			</div>
			<div
				class="flex h-full items-center justify-center rounded-lg border-2 bg-black"
				style:border-color={modalBudgetColor}
				style:color={modalBudgetColor}
			>
				<IconWrapper icon={modalBudgetIcon} classes="size-18">
					{#snippet fallback()}
						<Icon icon={ICONS_NAMES.pigBank} class="size-18" />
					{/snippet}
				</IconWrapper>
			</div>
		</div>
	</form>
	{#snippet footer()}
		<div class="flex justify-end gap-4">
			<button type="submit" form="new-wallet-form" class="primary-button px-4 py-2"> Create budget </button>
			<button class="primary-button-outline px-4 py-2" type="button" onclick={() => (showBudgetModal = false)}> Cancel </button>
		</div>
	{/snippet}
</Modal>

<section class="mt-12">
	<div class="flex items-center gap-4">
		<span style:color={data.wallet.color}>
			<Icon icon={data.wallet.iconify_name} class="size-16 stroke-2" />
		</span>
		<h1 class="text-5xl font-bold">{data.wallet.name}</h1>
		<hr class="flex-1 rounded-full border-4" style:border-color={data.wallet.color} />
	</div>
	<div class="my-10 grid grid-cols-4">
		<div class="flex items-center justify-between rounded-lg border-2 bg-black p-4" style:border-color={data.wallet.color}>
			<span style:color={data.wallet.color}>
				<Icon icon="ph:money-wavy" class="size-12" />
			</span>
			<span class="text-2xl font-bold"> {data.wallet.wallet_total}€ </span>
		</div>
	</div>
	<div class="grid grid-cols-3 gap-10">
		<div>
			<div class="flex items-center gap-2">
				<h2 class="text-3xl font-semibold">Budgets</h2>
				<button
					class="flex cursor-pointer items-center gap-1 rounded-lg border-2 p-1 font-semibold"
					style:border-color={data.wallet.color}
					onclick={openNewBudgetModal}
				>
					<Icon icon="qlementine-icons:plus-16" class="size-5" />
				</button>
			</div>
			<hr class="my-2 rounded-full border-2" style:border-color={data.wallet.color} />
			<form class="my-3 flex gap-10">
				<input
					type="text"
					class="flex-1 rounded-lg border-2 bg-black text-primary-50"
					placeholder="Filter by name"
					style:border-color={data.wallet.color}
					onchange={handleFilterBudgetNameOnChange}
				/>
				<div class="flex items-center gap-2">
					<p>Order by:</p>
					<select class="w-fit rounded-lg border-2 bg-black" style:border-color={data.wallet.color}>
						<option> Date </option>
						<option> Total </option>
					</select>
				</div>
			</form>
			<div class="space-y-4">
				{#if budgetsStore.loading}
					{#each [1, 2, 3] as i (i)}
						<div class="flex animate-pulse items-center gap-4 rounded-lg border-2 p-4" style:border-color={data.wallet.color}>
							<div class="size-10 rounded-xl" style:background-color={data.wallet.color}></div>
							<div class="h-9 flex-1 rounded-lg" style:background-color={data.wallet.color}></div>
							<div class="h-9 w-25 rounded-lg" style:background-color={data.wallet.color}></div>
						</div>
					{/each}
				{:else if budgetsStore.dataOut.length > 0}
					{#each budgetsStore.dataOut as budget (budget.id)}
						<div class="flex items-center gap-4 rounded-lg border-2 p-4">
							<div>
								<Icon icon={budget.iconify_name ?? ICONS_NAMES.pigBank} class="size-10" />
							</div>
							<div class="flex-1 text-xl font-semibold">{budget.name}</div>
							<div class="w-25 text-right">
								<span class="text-2xl font-bold">{budget.budget_total}</span><span class="text-base">€</span>
							</div>
						</div>
					{/each}
				{:else}
					<div class="flex items-center justify-center gap-4 rounded-lg border-4 border-primary-900 bg-primary-950 py-4 text-primary-100">
						<Icon icon={ICONS_NAMES.badSearch} class="size-8" />
						<p class="text-xl font-bold">No budgets match your search</p>
					</div>
				{/if}
			</div>
			{#if !budgetsStore.loading}
				<div class="mt-4 border-t-2 border-white/25">
					<div class="flex items-center justify-between px-4 py-1">
						<span>Total</span>
						<span><b>{budgetsStore.dataOut.reduce((acc, record) => acc + record.budget_total, 0)}</b><small>€</small></span>
					</div>
				</div>
			{/if}
		</div>
		<div class="col-span-2">
			<div class="flex items-center gap-2">
				<h2 class="text-3xl font-semibold">Movements</h2>
				<button class="flex cursor-pointer items-center gap-1 rounded-lg border-2 p-1 font-semibold" style:border-color={data.wallet.color}>
					<Icon icon="qlementine-icons:plus-16" class="size-5" />
				</button>
			</div>
			<hr class="my-2 rounded-full border-2" style:border-color={data.wallet.color} />
			<form class="my-3 flex gap-10">
				<input
					type="text"
					class="flex-1 rounded-lg border-2 bg-black text-primary-50"
					placeholder="Filter by name"
					style:border-color={data.wallet.color}
				/>
				<div class="flex items-center gap-2">
					<p>Order by:</p>
					<select class="w-fit rounded-lg border-2 bg-black" style:border-color={data.wallet.color}>
						<option> Date </option>
						<option> Amount </option>
						<option> Budget </option>
						<option> Category </option>
						<option> Title </option>
					</select>
				</div>
			</form>
			<div>
				<div class="movement-row border-b-4 py-2 font-bold">
					<div>Type</div>
					<div>Budget</div>
					<div class="flex items-center gap-2">Title</div>
					<div>Amount</div>
					<div>Balance</div>
					<div>Date</div>
				</div>
				{#each movementsStore.dataOut as mvt (mvt.id)}
					{@const mvtDate = new Date(mvt.done_at)}
					<div class="movement-row border-b-2 border-b-white/25 py-2 duration-150 last:border-b-0 hover:bg-primary-925">
						<div>
							{#if false}
								<Icon icon="ri:swap-box-fill" class="size-8 text-yellow-400" />
							{:else if mvt.is_deposit}
								<Icon icon="mdi:arrow-right-box" class="size-8 text-green-500" />
							{:else}
								<Icon icon="mdi:arrow-left-box" class="size-8 text-red-500" />
							{/if}
						</div>
						<div>{mvt.budget_name}</div>
						<div class="flex items-center gap-2">
							<!--{#if mvt.category}-->
							<!--	<span class="rounded-lg bg-white px-4 py-1 text-black"> {mvt.category} </span>-->
							<!--{/if}-->
							<span class="font-semibold"> {mvt.title} </span>
							{#if !mvt.is_manual}
								<span class="rounded bg-slate-700 px-2 py-1 text-xs italic opacity-50 select-none"> automatic </span>
							{/if}
						</div>
						<div class="text-right font-semibold">{mvt.amount}€</div>
						<div class="flex items-center justify-end gap-1 text-right">
							<span>{mvt.budget_balance}€</span>
							{#if mvt.is_manual}
								<Icon
									icon={mvt.is_deposit ? ICONS_NAMES.arrowUp : ICONS_NAMES.arrowDown}
									class={mvt.is_deposit ? "text-primary-400" : "text-red-500"}
								/>
							{:else}
								<Icon icon={ICONS_NAMES.dash} />
							{/if}
						</div>
						<div class="relative text-right">
							<small class="opacity-50">{mvtDate.toLocaleTimeString("en-GB").slice(0, 5)}</small>
							{mvtDate.toLocaleDateString("en-GB")}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
</section>

<style lang="postcss">
	@reference "tailwindcss";

	.movement-row {
		@apply gap-10;
		display: grid;
		grid-template-columns: 25px 0.15fr 0.85fr 100px 100px 125px;
		grid-auto-flow: column;
		align-items: center;
	}
</style>
