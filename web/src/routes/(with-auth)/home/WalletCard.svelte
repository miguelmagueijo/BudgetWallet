<script lang="ts">
	import Icon from "@iconify/svelte";

	let { title, budgets }: { title: string; budgets: Budget[] } = $props();

	const totalOfBudgets: number = budgets.reduce((total, b) => total + b.money, 0);
	const totalBudgetsStrParts = String(totalOfBudgets).split(".");
	const BAR_COLORS = ["#bb3e03", "#ca6702", "#ee9b00", "#e9d8a6", "#94d2bd"];
</script>

<div class="flex gap-8 rounded-lg border-2 border-[#00a1d9] bg-[#000000] p-6">
	<div class="flex items-center">
		<Icon icon="arcticons:trading-212" class="size-18 stroke-2 text-[#00a1d9]" />
	</div>
	<div class="flex-1 flex-col justify-between">
		<h3 class="text-2xl font-bold">{title}</h3>
		<div class="my-2">
			<div class="my-1 flex gap-1 overflow-hidden rounded-lg">
				{#each budgets as budget, idx (budget.title)}
					<div
						title={budget.title}
						class="h-2"
						style="width: {(budget.money / totalOfBudgets) * 100}%; background-color: {BAR_COLORS[idx % BAR_COLORS.length]}"
					></div>
				{/each}
			</div>
			<div class="flex items-center justify-between">
				<div class="budgets-info">
					<p class="text-white/50">
						<i class="text-xs">Budgets:</i> <b>{budgets.length}</b>
					</p>
					<Icon icon="ic:round-info" class="text-white/50" />
					<div class="budgets-info-tooltip">
						<ul>
							{#each budgets as budget, idx (budget.title)}
								<li>
									<span>{budget.title}</span>
									<span style="color: {BAR_COLORS[idx % BAR_COLORS.length]};"><b>{budget.money}</b><small>€</small></span>
								</li>
							{/each}
						</ul>
					</div>
				</div>
				<p class="text-right text-xl">
					<span class="font-bold text-[#00a1d9]">{totalBudgetsStrParts[0]}</span>{#if totalBudgetsStrParts.length > 1}<span
							class="text-sm text-[#00a1d9] opacity-75">.{totalBudgetsStrParts[1]}</span
						>{/if}
					<span class="text-sm">€</span>
				</p>
			</div>
			<!--<div class="text-xs opacity-50">Last change at: <b>20-02-2025</b></div>-->
		</div>
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

	.budgets-info-tooltip li span:first-child {
		font-style: italic;
	}
	.budgets-info-tooltip li span:last-child {
		@apply font-bold;
	}
</style>
