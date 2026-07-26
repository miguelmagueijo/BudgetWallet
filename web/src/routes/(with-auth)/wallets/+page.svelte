<script lang="ts">
	import Icon from "@iconify/svelte";
	import { DataStore } from "$lib/data.svelte";
	import { onMount } from "svelte";

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

	const walletsStore: DataStore<IWallet> = new DataStore<IWallet>("/api/wallets/?with_budgets=true");

	onMount(() => {
		walletsStore.load();
	});
</script>

<section>
	<a href="/home" class="mb-4 flex w-fit items-center gap-2 underline opacity-50">
		<Icon icon="pajamas:go-back" />
		<span>Home</span>
	</a>
	<h1 class="text-5xl font-bold">My wallets</h1>
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
				<div class="rounded-lg border-2 border-primary-0/25 bg-primary-950 p-4" style:border-color={wallet.color}>
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-2" style:color={wallet.color}>
							{#if wallet.icon}
								<Icon icon={wallet.icon} class="size-8 stroke-2" />
							{/if}
							<h2 class="text-xl font-bold">
								{wallet.name}
							</h2>
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
								<div class="flex justify-between rounded-lg border-2 border-primary-0/25 bg-primary-1000 p-4">
									<span class="font-bold">
										{budget.name}
									</span>
									<span>
										<b class:text-primary-500={budgetBalance > 0}>{budgetBalance}</b> <small>€</small>
									</span>
								</div>
							{:else}
								<div class="p-4 bg-primary-1000 rounded-lg text-primary-0/35">No budgets</div>
							{/each}
						{:else}
							sadsda
						{/if}
					</div>
				</div>
			{:else}
				<div>You don't have any wallets yet. Create one!</div>
			{/each}
		</div>
	{/if}
</section>
