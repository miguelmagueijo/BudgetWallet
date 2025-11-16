<script>
	import Icon from "@iconify/svelte";
	import WalletCard from "./WalletCard.svelte";
</script>

<section class="my-20">
	<h2 class="text-4xl font-bold mb-4">Hi, Miguel</h2>
	<div class="grid grid-cols-3 gap-8">
		<div class="info-card border-primary-400 text-primary-400 bg-primary-925">
			<Icon icon="ph:money-wavy" class="size-18"/>
			<div class="text-4xl font-bold text-right text-primary-50">2093<span class="text-lg font-semibold">.23€</span></div>

			<div class="info-card-tooltip">
				<span class="text-primary-950 bg-primary-400 after:border-b-primary-400">
					Total balance
				</span>
			</div>
		</div>
		<div class="p-4 bg-primary-400 rounded-lg text-primary-950 flex items-center justify-between relative">
			<Icon icon="mingcute:stock-line" class="size-18"/>
			<div class="text-4xl font-bold text-right">912<span class="text-lg font-semibold">.73€</span></div>
			<div class="absolute top-0 left-0 right-0 bottom-0 bg-black/90 z-90 flex items-center text-white">
				<div class="w-full text-center font-bold text-2xl text-primary-200">
					Coming soon...
				</div>
			</div>
		</div>
		<div class="p-4 bg-primary-400 rounded-lg text-primary-950 flex items-center justify-between relative">
			<Icon icon="fluent:money-calculator-20-regular" class="size-18"/>
			<div class="text-4xl font-bold text-right">0.10<span class="text-lg font-semibold">€/day</span></div>
			<div class="absolute top-0 left-0 right-0 bottom-0 bg-black/90 z-90 flex items-center text-white">
				<div class="w-full text-center font-bold text-2xl text-primary-200">
					Coming soon...
				</div>
			</div>
		</div>
	</div>
</section>

<style lang="postcss">
    @reference "tailwindcss";

    .info-card {
		@apply p-4 border-2 rounded-lg;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

    .info-card-tooltip {
        position: absolute;
		left: 50%;
		top: 100%;
		visibility: hidden;
		transform: translateX(-50%);
    }

    .info-card-tooltip > span {
        @apply py-2 px-4 rounded-lg font-semibold border-2 mt-4;
		display: block;
		text-align: center;
		border-color: transparent;
		width: fit-content;
    }

    .info-card-tooltip > span::after {
        content: "";
        position: absolute;
        top: -3px;
        left: 50%;
		transform: translateX(-50%);
        border-width: 10px;
        border-style: solid;
		border-left-color: transparent;
		border-right-color: transparent;
		border-top-color: transparent;
    }

    .info-card:hover .info-card-tooltip {
		visibility: visible;
	}
</style>

<section>
	<div class="flex items-end justify-between">
		<h2 class="text-4xl font-bold">Your wallets</h2>
		<button
			type="button"
			class="primary-button-outline flex items-center gap-1 py-2 px-4"
		>
			<span>New Wallet</span>
			<Icon icon="typcn:plus" class="size-5" />
		</button>
	</div>
	<div class="my-4">
		<form class="flex items-center gap-4">
			<div class="flex border-2 border-primary-700 bg-black w-fit rounded-lg items-center p-1 px-2">
				<Icon icon="ic:baseline-search" class="size-6 text-primary-700"/>
				<input type="text" class="bg-transparent rounded-lg border-0 text-white w-[450px] focus:ring-0" placeholder="Filter by name"/>
			</div>
			<div>
				<select class="w-[150px] border-2 border-primary-700 p-3 text-green-100 rounded-lg bg-black font-semibold">
					<!-- TODO: implement favorites -->
					<!-- <option>Favorites</option> -->
					<option>Name</option>
					<option>Balance</option>
				</select>
			</div>
		</form>
	</div>
	<div class="mt-6 grid grid-cols-4 gap-10">
		<WalletCard
			id={1}
			title="Trading 212"
			iconName="arcticons:trading-212"
			color="#00a1d9"
			budgets={[
				{ title: "New monitor", money: 291.2 },
				{ title: "Car fix", money: 523.2 },
			]}
		/>
		<WalletCard
			id={2}
			title="Trade Republic"
			iconName="arcticons:traderepublic"
			color="#FFFFFF"
			budgets={[
				{ title: "New monitor", money: 291.2 },
				{ title: "Car fix", money: 523.2 },
				{ title: "Television", money: 923.23 },
				{ title: "TV2", money: 923.23 },
				{ title: "TV3", money: 923.23 },
			]}
		/>
		<WalletCard
			id={3}
			title="Caixa Agricola"
			iconName="arcticons:camobile"
			color="#009257"
			budgets={[
				{ title: "New monitor", money: 291.2 },
				{ title: "Car fix", money: 523.2 },
				{ title: "Television", money: 923.23 },
			]}
		/>
		<WalletCard
			id={4}
			title="Moey!"
			iconName="arcticons:moey"
			color="#c3f261"
			budgets={[
				{ title: "Television", money: 923.23 },
			]}
		/>
		<WalletCard
			id={4}
			title="Revolut"
			iconName="arcticons:revolut"
			color="#FFFFFF"
			budgets={[
				{ title: "New monitor", money: 291.2 },
				{ title: "Car fix", money: 523.2 },
				{ title: "Television", money: 923.23 },
			]}
		/>
		<!--		<div class="flex gap-8 rounded-lg border-2 border-white bg-black p-6">-->
		<!--			<div class="flex items-center">-->
		<!--				<Icon icon="arcticons:traderepublic" class="size-18 stroke-2 text-white" />-->
		<!--			</div>-->
		<!--			<div>-->
		<!--				<h3 class="text-2xl font-bold">Trade Republic</h3>-->
		<!--				<div class="flex items-center gap-1">-->
		<!--					<p>Budgets: 5</p>-->
		<!--					<Icon icon="ic:round-info" />-->
		<!--				</div>-->
		<!--				<p>-->
		<!--					Money: <span class="font-bold">5000</span> <small>€</small>-->
		<!--				</p>-->
		<!--			</div>-->
		<!--		</div>-->
	</div>
</section>
