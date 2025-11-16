<script lang="ts">
	import { resolve } from "$app/paths";
	import Icon from "@iconify/svelte";
</script>

<a href={resolve("/home")} class="flex w-fit items-center gap-1 border-b-1">
	<Icon icon="lets-icons:back" />
	<span> Home </span>
</a>

<section class="mt-12">
	<div class="flex items-center gap-4">
		<Icon icon="arcticons:trading-212" class="size-16 stroke-2 text-[#00a1d9]" />
		<h1 class="text-5xl font-bold">Trading 212</h1>
		<hr class="flex-1 rounded-full border-4 border-[#00a1d9]" />
	</div>
	<div class="grid grid-cols-3 gap-10">
		<div class="mt-10">
			<h2 class="text-4xl font-semibold">Budgets</h2>
			<hr class="my-2 rounded-full border-2 border-[#00a1d9]" />
			<form class="my-3 flex gap-2">
				<input type="text" class="flex-1 rounded-lg border-2 border-[#00a1d9] bg-black text-primary-50" placeholder="Filter by name" />
				<select class="w-[150px] rounded-lg border-2 border-[#00a1d9] bg-black">
					<option> by name </option>
					<option> by total </option>
				</select>
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
		<div class="col-span-2 mt-10">
			<h2 class="text-3xl font-semibold">Movements</h2>
			<hr class="my-2 rounded-full border-2 border-[#00a1d9]" />
			<div>- 1</div>
		</div>
	</div>
</section>
