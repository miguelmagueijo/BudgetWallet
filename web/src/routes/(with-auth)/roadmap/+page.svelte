<script lang="ts">
	import { version } from "$app/environment";

	interface RoadmapItem {
		version: string;
		features: string[];
	}

	const data: Array<RoadmapItem> = [
		{
			version: "0.0",
			features: ["Development"],
		},
		{
			version: "0.1",
			features: ["Wallets", "Budgets", "Movements", "Movements categories", "Roadmap page", "Basic user settings"],
		},
		{
			version: "0.2",
			features: ["Move budgets between wallets (with or without movements)", "Basic statistics"],
		},
		{
			version: "0.3",
			features: ["Responsiveness", "PWA version", "Allow user registration by invites", "Publish on LinkedIn"],
		},
		{
			version: "0.4",
			features: ["Money splitter", "Monthly/Yearly Subscriptions"],
		},
		{
			version: "0.5",
			features: ["To buy list (alone or group)", "Loans to other people (user or not)"],
		},
		{
			version: "0.6",
			features: ["Wallets/Budget interest system", "Quick interest calculator"],
		},
		{
			version: "0.7",
			features: ["Simple investments register", "Allow user to export Excel/PDF files"],
		},
		{
			version: "0.8",
			features: ["Calendar"],
		},
	];
</script>

<section class="mx-auto mt-10 w-180">
	<h1 class="text-center text-6xl font-bold">Roadmap</h1>
	<h2 class="text-center text-lg opacity-50">of Budget Wallet</h2>
	<div class="mt-8 flex items-center justify-center gap-2">
		<div class="size-4 rounded-full bg-white"></div>
		<i class="opacity-75">Current version</i>
	</div>
	<div class="relative mt-4 grid grid-flow-row grid-cols-2 gap-x-24 gap-y-10 pt-12 pb-32">
		<div class="absolute top-0 left-1/2 h-full w-4 -translate-x-1/2 rounded-lg bg-primary-900"></div>
		{#each data as item, idx (idx)}
			{@const isLeft = idx % 2 !== 0}
			{@const isCurrent = version.startsWith(item.version)}
			{#if isLeft}
				<div></div>
			{/if}
			<div>
				<div class="relative rounded-lg {isCurrent ? 'bg-white text-primary-950' : 'bg-primary-700'}  p-4">
					<div
						class="absolute top-1/2 {isLeft ? '-left-17' : '-right-17'} size-10 -translate-y-1/2 rounded-full {isCurrent
							? 'bg-white'
							: 'bg-primary-900'}"
					></div>
					<h3 class="{isLeft ? '' : 'text-right'} text-xl font-bold italic">Version {item.version}.x</h3>
				</div>
				<div class="mt-4 rounded-lg bg-primary-910 p-4">
					<ul class="list-disc space-y-2 pl-4">
						{#each item.features as feat, fIdx (fIdx)}
							<li>{feat};</li>
						{/each}
					</ul>
				</div>
			</div>
			{#if !isLeft}
				<div></div>
			{/if}
		{/each}
	</div>
</section>
