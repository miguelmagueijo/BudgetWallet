<script lang="ts">
	import { resolve } from "$app/paths";
	import Icon from "@iconify/svelte";
	import { DataStore } from "$lib/data.svelte";
	import { onMount } from "svelte";
	import { ICONS_NAMES } from "$lib";
	import type { ChangeEventHandler } from "svelte/elements";

	interface IBudgetSimpleInfo {
		id: string;
		name: string;
		iconify_name: string;
		color: string;
		is_permanent: boolean;
		budget_total: number;
	}

	const movementData = [
		{
			id: 1,
			type: "OUT",
			budget: "Steam Deck",
			category: "Shops",
			title: "New mice",
			total: -29.99,
			date: "29/01/2025",
		},
		{
			id: 2,
			type: "MANUAL",
			budget: "Steam Deck",
			category: null,
			title: "Fix money",
			total: -290.93,
			date: "01/01/2025",
		},
		{
			id: 3,
			type: "OUT",
			budget: "Steam Deck",
			category: null,
			title: "Transfer to friend",
			total: -50,
			date: "29/01/2025",
		},
		{
			id: 4,
			type: "IN",
			budget: "Steam Deck",
			category: "Income",
			title: "Monthly income",
			total: 500,
			date: "29/01/2025",
		},
	];

	const { data } = $props();

	let budgetsStore = new DataStore<IBudgetSimpleInfo>(true);

	function fetchBudgets(ignoreLoadingFlag: boolean = false) {
		if (!ignoreLoadingFlag && budgetsStore.loading) {
			return;
		}

		budgetsStore.loading = true;

		fetch(`/api/budgets/${data.wallet.id}`, {
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

	const handleFilterBudgetNameOnChange: ChangeEventHandler<HTMLInputElement> = (event) => {
		const value = event.currentTarget.value;

		if (!value) {
			budgetsStore.resetFilter();
		} else {
			budgetsStore.applyFilter((element) => element.name.toLowerCase().includes(value.toLowerCase()));
		}
	};

	onMount(() => {
		fetchBudgets(true);
	});
</script>

<svelte:head>
	<title>BW | {data.wallet.name}</title>
</svelte:head>

<a href={resolve("/home")} class="flex w-fit items-center gap-1 border-b text-lg">
	<Icon icon="lets-icons:back" />
	<span> Home </span>
</a>

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
			<h2 class="text-4xl font-semibold">Budgets</h2>
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
				{:else}
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
			<h2 class="text-3xl font-semibold">Movements</h2>
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
					<div class="text-right">Amount</div>
					<div class="text-right">Balance</div>
					<div class="text-right">Date</div>
				</div>
				{#each movementData as mvt (mvt.id)}
					<div class="movement-row border-b-2 border-b-white/25 py-2 last:border-b-0">
						<div>
							{#if mvt.type === "OUT"}
								<Icon icon="mdi:arrow-left-box" class="size-8 text-red-500" />
							{:else if mvt.type === "IN"}
								<Icon icon="mdi:arrow-right-box" class="size-8 text-green-500" />
							{:else}
								<Icon icon="ri:swap-box-fill" class="size-8 text-yellow-400" />
							{/if}
						</div>
						<div>{mvt.budget}</div>
						<div class="flex items-center gap-2">
							{#if mvt.category}
								<span class="rounded-lg bg-white px-4 py-1 text-black"> {mvt.category} </span>
							{/if}
							<span class="font-semibold"> {mvt.title} </span>
						</div>
						<div class="text-right font-semibold {mvt.total > 0 ? 'text-primary-400' : 'text-red-500'}">{mvt.total}€</div>
						<div class="text-right">2000€</div>
						<div class="text-right">{mvt.date}</div>
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
		grid-template-columns: 100px 0.15fr 0.85fr 100px 100px 100px;
		grid-auto-flow: column;
		align-items: center;
	}
</style>
