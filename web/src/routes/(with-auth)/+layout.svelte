<script lang="ts">
	import "../../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import Icon from "@iconify/svelte";
	import { resolve } from "$app/paths";
	import { version } from "$app/environment";
	import type { LayoutProps } from "./$types";
	import { ICONS_NAMES } from "$lib";

	let { data, children }: LayoutProps = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen flex-col">
	<nav class="flex items-center justify-between bg-primary-925 px-6 py-4">
		<a href={resolve("/home")} class="flex items-center gap-2 text-xl font-bold text-[#30EB72]">
			<Icon icon="streamline-ultimate:money-wallet-open-bold" />
			Budget Wallet
		</a>
		<div class="flex items-center gap-4">
			<div class="group relative">
				<div
					class="flex items-center justify-between gap-4 rounded-lg border-2 border-transparent bg-primary-1000 px-3 py-2 group-hover:rounded-b-none group-hover:border-primary-900 group-hover:border-b-primary-1000"
				>
					<b class="capitalize">{data.user.username}</b>
					<div class="flex size-8 items-center justify-center rounded-full bg-primary-0 text-primary-1000 select-none">
						{data.user.username.charAt(0).toUpperCase()}
					</div>
				</div>
				<div class="absolute top-full right-0 hidden w-62 group-hover:block">
					<div class="text-normal -mt-0.5 rounded-lg rounded-tr-none border-2 border-primary-900 bg-primary-1000 p-4">
						<ul class="space-y-3">
							<li>
								<a
									href={resolve("/account/settings/")}
									class="flex items-center gap-2 rounded-lg px-2 py-1 font-semibold duration-300 hover:bg-primary-0 hover:text-primary-1000"
								>
									<Icon icon={ICONS_NAMES.accountSettings} class="size-5" />
									<span>Account settings</span>
								</a>
							</li>
							<li>
								<!-- eslint-disable svelte/no-navigation-without-resolve -->
								<a
									href="/logout"
									class="flex items-center gap-2 rounded-lg px-2 py-1 font-semibold text-red-500 duration-300 hover:bg-red-500 hover:text-red-950"
								>
									<Icon icon={ICONS_NAMES.logout} class="size-5 stroke-2" />
									<span>Logout</span>
								</a>
							</li>
						</ul>
					</div>
				</div>
			</div>
		</div>
	</nav>

	<main class="mb-20 flex-1 p-6">
		{@render children()}
	</main>

	<footer class="mt-auto border-t-2 border-t-white/10 bg-primary-950 p-6">
		<a href={resolve("/home")} class="flex w-fit items-center gap-2 text-lg font-bold text-[#30EB72]">
			<Icon icon="streamline-ultimate:money-wallet-open-bold" />
			Budget Wallet
		</a>
		<div class="flex items-start justify-between">
			<div>
				<div class="text-sm text-green-200 italic">Keep your money tracked across your apps and banks.</div>
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
			<div class="flex gap-8">
				<div class="min-w-35">
					<p class="border-b border-b-white/25 text-base font-semibold">Budget Wallet</p>
					<ul class="mt-2 text-sm opacity-75">
						<li><a href={resolve("/home")}>Home</a></li>
						<li><a href={resolve("/roadmap")}>Roadmap</a></li>
					</ul>
				</div>
				<div class="min-w-35">
					<p class="border-b border-b-white/25 text-base font-semibold">Account</p>
					<ul class="mt-2 text-sm opacity-75">
						<li><a href={resolve("/account/settings")}>Settings</a></li>
						<li><a href="/logout">Logout</a></li>
					</ul>
				</div>
			</div>
		</div>
		<div class="mt-10 flex justify-between text-xs opacity-50">
			<div>
				Developed by
				<a href="https://miguelmagueijo.pt" class="font-bold underline" target="_blank"> Miguel Magueijo </a>
			</div>
			<i>V{version}</i>
		</div>
	</footer>
</div>
