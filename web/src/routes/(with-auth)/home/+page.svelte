<script>
	import Icon from "@iconify/svelte";
	import WalletCard from "./WalletCard.svelte";
</script>

<section class="mb-12">
	<h2 class="text-4xl">Hi, Miguel</h2>
	<p>Here some stats about your wallets!</p>
	<div>Balance: 5000€</div>
</section>

<section>
	<div class="flex items-end justify-between">
		<h2 class="text-4xl font-bold">Your wallets</h2>
		<button
			type="button"
			class="flex cursor-pointer items-center gap-1 rounded-lg border-2 border-[#30EB72] px-2 py-1 font-semibold text-[#30EB72] duration-300 hover:bg-[#30EB72] hover:text-green-950"
		>
			<span>New Wallet</span>
			<Icon icon="typcn:plus" class="size-5" />
		</button>
	</div>
	<div class="mt-6 grid grid-cols-4 gap-10">
		<WalletCard
			title="Trading 212"
			budgets={[
				{ title: "New monitor", money: 291.2 },
				{ title: "Car fix", money: 523.2 },
				{ title: "Television", money: 923.23 },
			]}
		/>
		<div class="flex gap-8 rounded-lg border-2 border-white bg-black p-6">
			<div class="flex items-center">
				<Icon icon="arcticons:traderepublic" class="size-18 stroke-2 text-white" />
			</div>
			<div>
				<h3 class="text-2xl font-bold">Trade Republic</h3>
				<div class="flex items-center gap-1">
					<p>Budgets: 5</p>
					<Icon icon="ic:round-info" />
				</div>
				<p>
					Money: <span class="font-bold">5000</span> <small>€</small>
				</p>
			</div>
		</div>
	</div>
</section>
