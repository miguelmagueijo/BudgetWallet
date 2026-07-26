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
		<div>A carregar dados...</div>
	{:else}
		<div class="mt-12 flex flex-col gap-6">
			{#each walletsStore.dataOut as wallet (wallet.id)}
				<div class="rounded-lg border-2 border-primary-0/25 p-4" style:border-color={wallet.color}>
					<div class="flex items-center gap-2" style:color={wallet.color}>
						{#if wallet.icon}
							<Icon icon={wallet.icon} class="size-8 stroke-2" />
						{/if}
						<h2 class="text-xl font-bold">
							{wallet.name}
						</h2>
					</div>
				</div>
			{:else}
				<div>You don't have any wallets yet. Create one!</div>
			{/each}
		</div>
	{/if}
</section>
