<script lang="ts">
	import { resolve } from "$app/paths";
	import Icon from "@iconify/svelte";
</script>

<a href={resolve("/home")} class="border-b-1 flex gap-1 w-fit items-center">
	<Icon icon="lets-icons:back"/>
	<span>
		Home
	</span>
</a>

<section class="mt-12">
	<div class="opacity-50">
		Wallet
	</div>
	<div class="flex gap-4 items-center">
		<Icon icon="arcticons:trading-212" class="text-[#00a1d9] size-16 stroke-2"/>
		<h1 class="text-5xl font-bold">
			Trading 212
		</h1>
		<hr class="border-4 border-[#00a1d9] flex-1 rounded-full"/>
	</div>
	<div class="grid grid-cols-2 gap-10">
		<div class="mt-10">
			<h2 class="text-3xl font-semibold">Budgets</h2>
			<div>
				- 1
			</div>
		</div>
		<div class="mt-10">
			<h2 class="text-3xl font-semibold">Movements</h2>
			<div>
				- 1
			</div>
		</div>
	</div>
</section>