<script lang="ts">
	import Icon from "@iconify/svelte";
	import WalletCard from "./WalletCard.svelte";
	import Modal from "$lib/components/Modal.svelte";
	import IconWrapper from "$lib/components/IconWrapper.svelte";

	const DEFAULT_WALLET_ICON = "streamline-ultimate:money-wallet-open-bold";

	let showAddWalletModal = $state(false);
	let newWalletColor = $state("#FFFFFF");
	let newWalletIcon = $state(DEFAULT_WALLET_ICON);
	let newWalletDescription = $state("");
	let newWalletMoney = $state(0);
</script>

<Modal bind:showModal={showAddWalletModal} title="New wallet">
	<form class="max-w-[500px] space-y-2">
		<div>
			<label class="block font-semibold" for="wallet-name"> Name <span class="text-red-500">*</span> </label>
			<input id="wallet-name" name="walletName" type="text" class="w-full rounded-lg border-2 border-primary-900 bg-black" required />
			<small class="opacity-50"> Min 3 characters </small>
		</div>
		<div>
			<label class="block font-semibold" for="wallet-desc"> Start balance <span class="text-red-500">*</span> </label>
			<input
				id="wallet-money"
				name="walletMoney"
				class="w-full rounded-lg border-2 border-primary-900 bg-black"
				type="number"
				bind:value={newWalletMoney}
				required
			/>
		</div>
		<div>
			<label class="block font-semibold" for="wallet-desc"> Description </label>
			<textarea
				id="wallet-desc"
				name="walletDesc"
				class="max-h-[200px] w-full rounded-lg border-2 border-primary-900 bg-black"
				maxlength="512"
				bind:value={newWalletDescription}
			></textarea>
			<small class="flex justify-between opacity-50">
				<span>Max 512</span>
				<span>Total: {newWalletDescription.length}</span>
			</small>
		</div>
		<div class="grid grid-cols-3 gap-4">
			<div class="col-span-2">
				<div>
					<label class="block font-semibold" for="wallet-color"> Icon </label>
					<input
						id="wallet-color"
						name="walletColor"
						type="color"
						class="w-full rounded-lg border-2 border-primary-900 bg-black h-11"
						bind:value={newWalletColor}
					/>
				</div>
				<div class="mt-2">
					<label class="block font-semibold" for="wallet-color"> Icon </label>
					<input
						id="wallet-color"
						name="walletColor"
						type="text"
						class="w-full rounded-lg border-2 border-primary-900 bg-black"
						bind:value={newWalletIcon}
					/>
					<small class="opacity-50">
						Icon name from: <a class="font-bold underline" href="https://icon-sets.iconify.design/" target="_blank">Iconify</a>
					</small>
				</div>
			</div>
			<div
				class="flex h-full items-center justify-center rounded-lg border-2 bg-black"
				style="border-color: {newWalletColor}; color: {newWalletColor};"
			>
				<IconWrapper icon={newWalletIcon} classes="size-18">
					{#snippet fallback()}
						<Icon icon={DEFAULT_WALLET_ICON} class="size-18" />
					{/snippet}
				</IconWrapper>
			</div>
		</div>
	</form>
	{#snippet footer()}
		<button type="button">
			Cancel
		</button>
		<button type="button">
			Create
		</button>
	{/snippet}
</Modal>

<section class="my-20">
	<h2 class="mb-4 text-5xl font-bold">Hi, Miguel</h2>
	<div class="grid grid-cols-3 gap-8">
		<div class="info-card border-primary-400 bg-primary-925 text-primary-400">
			<Icon icon="ph:money-wavy" class="size-18" />
			<div class="text-right text-4xl font-bold text-primary-50">2093<span class="text-lg font-semibold">.23€</span></div>

			<div class="info-card-tooltip">
				<span class="bg-primary-400 text-primary-950 after:border-b-primary-400"> Total balance </span>
			</div>
		</div>
		<div class="relative flex items-center justify-between rounded-lg bg-primary-400 p-4 text-primary-950">
			<Icon icon="mingcute:stock-line" class="size-18" />
			<div class="text-right text-4xl font-bold">912<span class="text-lg font-semibold">.73€</span></div>
			<div class="absolute top-0 right-0 bottom-0 left-0 z-90 flex items-center bg-black/90 text-white">
				<div class="w-full text-center text-2xl font-bold text-primary-200">Coming soon...</div>
			</div>
		</div>
		<div class="relative flex items-center justify-between rounded-lg bg-primary-400 p-4 text-primary-950">
			<Icon icon="fluent:money-calculator-20-regular" class="size-18" />
			<div class="text-right text-4xl font-bold">0.10<span class="text-lg font-semibold">€/day</span></div>
			<div class="absolute top-0 right-0 bottom-0 left-0 z-90 flex items-center bg-black/90 text-white">
				<div class="w-full text-center text-2xl font-bold text-primary-200">Coming soon...</div>
			</div>
		</div>
	</div>
</section>

<section>
	<div class="flex items-end justify-between">
		<h2 class="text-4xl font-bold">Your wallets</h2>
		<button type="button" class="primary-button-outline flex items-center gap-1 px-4 py-2" onclick={() => (showAddWalletModal = true)}>
			<span>New Wallet</span>
			<Icon icon="typcn:plus" class="size-5" />
		</button>
	</div>
	<div class="my-4">
		<form class="flex items-center gap-4">
			<div class="flex w-fit items-center rounded-lg border-2 border-primary-700 bg-black p-1 px-2">
				<Icon icon="ic:baseline-search" class="size-6 text-primary-700" />
				<input type="text" class="w-[450px] rounded-lg border-0 bg-transparent text-white focus:ring-0" placeholder="Filter by name" />
			</div>
			<div>
				<select class="w-[150px] rounded-lg border-2 border-primary-700 bg-black p-3 font-semibold text-green-100">
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
		<WalletCard id={4} title="Moey!" iconName="arcticons:moey" color="#c3f261" budgets={[{ title: "Television", money: 923.23 }]} />
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

<style lang="postcss">
	@reference "tailwindcss";

	.info-card {
		@apply rounded-lg border-2 p-4;
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
		@apply mt-4 rounded-lg border-2 px-4 py-2 font-semibold;
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
