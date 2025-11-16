<script lang="ts">
	import "../../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import Icon from "@iconify/svelte";
	import { resolve } from "$app/paths";

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen flex-col">
	<nav class="flex items-center justify-between bg-primary-925 p-6">
		<a href={resolve("/home")} class="flex items-center gap-2 text-xl font-bold text-[#30EB72]">
			<Icon icon="streamline-ultimate:money-wallet-open-bold" />
			Budget Wallet
		</a>
	</nav>

	<main class="flex-1 p-6">
		{@render children()}
	</main>

	<footer class="mt-auto border-t-2 border-t-white/10 bg-primary-950 p-6">
		<div class="flex items-center justify-between">
			<div>
				<a
					href={resolve("/home")}
					class="flex items-center gap-2 text-lg font-bold text-[#30EB72]"
				>
					<Icon icon="streamline-ultimate:money-wallet-open-bold" />
					Budget Wallet
				</a>
				<div class="text-sm text-green-200 italic">
					Keep your money tracked across your apps and banks.
				</div>
				<div class="text-green-200">
					<div class="mt-2 flex items-center">
						<a
							href="https://github.com/miguelmagueijo/BudgetWallet"
							target="_blank"
							class="duration-150 hover:scale-125 hover:text-[#30EB72]"
						>
							<Icon icon="mingcute:github-fill" class="size-4" />
						</a>
					</div>
				</div>
			</div>
		</div>
		<div class="mt-2 text-xs opacity-50">
			Developed by
			<a href="https://miguelmagueijo.pt" class="font-bold underline" target="_blank">
				Miguel Magueijo
			</a>
		</div>
	</footer>
</div>
