<script lang="ts">
	import { resolve } from "$app/paths";
	import Icon from "@iconify/svelte";

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
</script>

<a href={resolve("/home")} class="flex w-fit items-center gap-1 border-b-1 text-lg">
	<Icon icon="lets-icons:back" />
	<span> Home </span>
</a>

<section class="mt-12">
	<div class="flex items-center gap-4">
		<Icon icon="arcticons:trading-212" class="size-16 stroke-2 text-[#00a1d9]" />
		<h1 class="text-5xl font-bold">Trading 212</h1>
		<hr class="flex-1 rounded-full border-4 border-[#00a1d9]" />
	</div>
	<div class="my-10 grid grid-cols-4">
		<div class="flex items-center justify-between rounded-lg border-2 border-[#00a1d9] bg-black p-4">
			<Icon icon="ph:money-wavy" class="size-12" />
			<span class="text-2xl font-bold"> 2392.23€ </span>
		</div>
	</div>
	<div class="grid grid-cols-3 gap-10">
		<div>
			<h2 class="text-4xl font-semibold">Budgets</h2>
			<hr class="my-2 rounded-full border-2 border-[#00a1d9]" />
			<form class="my-3 flex gap-10">
				<input type="text" class="flex-1 rounded-lg border-2 border-[#00a1d9] bg-black text-primary-50" placeholder="Filter by name" />
				<div class="flex items-center gap-2">
					<p>Order by:</p>
					<select class="w-fit rounded-lg border-2 border-[#00a1d9] bg-black">
						<option> Date </option>
						<option> Total </option>
					</select>
				</div>
			</form>
			<div class="space-y-4">
				<div class="flex items-center gap-4 rounded-lg border-2 border-white p-4">
					<div>
						<Icon icon="fa6-solid:piggy-bank" class="size-10" />
					</div>
					<div class="flex-1 text-xl font-semibold">Money</div>
					<div class="w-[175px] text-right">
						<span class="text-2xl font-bold">9283.83</span><span class="text-base">€</span>
					</div>
				</div>
				<div class="flex items-center gap-4 rounded-lg border-2 border-white p-4">
					<div>
						<Icon icon="ic:round-laptop" class="size-10" />
					</div>
					<div class="flex-1 text-xl font-semibold">New laptop</div>
					<div class="w-[100px] text-right">
						<span class="text-2xl font-bold">800</span><span class="text-base">€</span>
					</div>
				</div>
				<div class="flex items-center gap-4 rounded-lg border-2 border-white p-4">
					<div>
						<Icon icon="simple-icons:steamdeck" class="size-10" />
					</div>
					<div class="flex-1 text-xl font-semibold">Steam Deck</div>
					<div class="w-[100px] text-right">
						<span class="text-2xl font-bold">200</span><span class="text-base">€</span>
					</div>
				</div>
			</div>
			<div class="mt-4 border-t-2 border-white/25">
				<div class="flex items-center justify-between px-4 py-1">
					<span>Total</span>
					<span><b>1308.83</b><small>€</small></span>
				</div>
			</div>
		</div>
		<div class="col-span-2">
			<h2 class="text-3xl font-semibold">Movements</h2>
			<hr class="my-2 rounded-full border-2 border-[#00a1d9]" />
			<form class="my-3 flex gap-10">
				<input type="text" class="flex-1 rounded-lg border-2 border-[#00a1d9] bg-black text-primary-50" placeholder="Filter by name" />
				<div class="flex items-center gap-2">
					<p>Order by:</p>
					<select class="w-fit rounded-lg border-2 border-[#00a1d9] bg-black">
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
