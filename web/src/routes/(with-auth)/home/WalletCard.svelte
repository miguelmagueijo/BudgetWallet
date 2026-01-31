<script lang="ts">
	import Icon from "@iconify/svelte";
	import { resolve } from "$app/paths";

	// TODO: try to only require the CardWalletData
	interface Props {
		id: number;
		title: string;
		iconName: string;
		color: string;
		totalMoney: number;
		budgets: Array<CardWalletBudgetData>;
	}

	export interface CardWalletBudgetData {
		id: number;
		name: string;
		color?: string;
		total: number;
	}

	export interface CardWalletData {
		id: number;
		name: string;
		icon?: string;
		color?: string;
		budgets: Array<CardWalletBudgetData>;
		total_money: number;
	}

	let { id, title, iconName, color, budgets, totalMoney }: Props = $props();

	const totalBudgetsStrParts = String(totalMoney.toFixed(2)).split(".").map(Number);
	const BAR_COLORS = ["#dafbfa", "#7dcecc", "#467876", "#213d3c"];
	const detailsRouteResolved = resolve(`/wallet/${id}`);

	function getBarColor(idx: number, color: string | undefined) {
		if (color) {
			return color;
		} else {
			return BAR_COLORS[idx % BAR_COLORS.length];
		}
	}
</script>

<div
	class="flex animate-pulse items-center gap-4 rounded-lg border-2 bg-black p-6"
	class:border-primary-900={id < 0}
	class:animate-pulse={id < 0}
	style:border-color={color ? color : ""}
>
	{#if id < 0}
		<div class="size-20 rounded-lg bg-primary-900"></div>
	{:else}
		<a href={detailsRouteResolved} class="flex w-fit items-center">
			<Icon icon={iconName} class="size-20 stroke-2" style="color: {color}" />
		</a>
	{/if}
	<div class="flex-1">
		{#if id < 0}
			<div class="h-[24px] w-full rounded-lg bg-primary-900"></div>
			<div class="mt-2 h-12 w-full rounded-lg bg-primary-900"></div>
		{:else}
			<a href={detailsRouteResolved} class="hover:underline">
				<h3 class="text-2xl font-bold text-white">{title}</h3>
			</a>
			<div class="mt-auto">
				<div class="my-1 flex gap-1 overflow-hidden rounded-lg">
					{#if totalMoney > 0}
						{#each budgets as budget, idx (budget.id)}
							<div
								title={budget.name}
								class="h-2"
								style="width: {(budget.total / totalMoney) * 100}%; background-color: {getBarColor(idx, budget.color)}"
							></div>
						{/each}
					{/if}
				</div>
				<div class="flex items-center justify-between">
					<div class="budgets-info">
						<p class="text-white/50 select-none">
							<i class="text-xs">Budgets:</i> <b>{budgets.length}</b>
						</p>
						<Icon icon="ic:round-info" class="text-white/50" />
						<div class="budgets-info-tooltip">
							<ul>
								{#each budgets as budget, idx (budget.id)}
									<li>
										<i>{budget.name}</i>
										<b style="color: {getBarColor(idx, budget.color)};"><b>{budget.total}</b><small>€</small></b>
									</li>
								{/each}
							</ul>
						</div>
					</div>
					<p class="text-right text-xl">
						<span class="font-bold" style="color: {color}">{totalBudgetsStrParts[0]}</span>{#if totalBudgetsStrParts[1] !== 0}<span
								class="text-sm opacity-75"
								style="color: {color}">.{totalBudgetsStrParts[1]}</span>{/if}
						<span class="text-sm">€</span>
					</p>
				</div>
				<!--<div class="text-xs opacity-50">Last change at: <b>20-02-2025</b></div>-->
			</div>
		{/if}
	</div>
</div>

<style lang="postcss">
	@reference "tailwindcss";

	.budgets-info {
		@apply gap-0.5 text-sm;
		text-align: right;
		display: flex;
		align-items: center;
		position: relative;
	}

	.budgets-info:hover .budgets-info-tooltip {
		display: block;
	}

	.budgets-info-tooltip {
		@apply pt-1;
		color: white;
		position: absolute;
		top: 100%;
		left: 0;
		width: 222px;
		display: none;
		z-index: 100;
	}

	.budgets-info-tooltip > ul {
		@apply rounded-lg border border-white bg-black p-2;
		text-align: left;
	}

	.budgets-info-tooltip li {
		@apply gap-1 border-b border-b-white/20;
		display: flex;
		justify-content: space-between;
	}

	.budgets-info-tooltip li:last-child {
		border: none !important;
	}
</style>
