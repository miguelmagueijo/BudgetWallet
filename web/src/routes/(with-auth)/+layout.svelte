<script lang="ts">
	import "../../app.css";
	import favicon from "$lib/assets/favicon.svg";
	import Icon from "@iconify/svelte";
	import { version } from "$app/environment";
	import type { LayoutProps } from "./$types";
	import { ICONS_NAMES } from "$lib";
	import Toast from "$lib/components/Toast.svelte";
	import { ToastStore } from "$lib/toast.svelte";
	import { setContext } from "svelte";

	let { children }: LayoutProps = $props();
	const toastStore = new ToastStore();

	setContext("toastStore", toastStore);
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div class="flex h-screen overflow-auto">
	<nav class="sticky top-0 z-10 flex h-screen w-24 flex-col items-center justify-between bg-primary-925 p-6">
		<div class="flex flex-col">
			<a href="/home" class="rounded-xl bg-primary-600 p-4 text-primary-0">
				<Icon icon="streamline-ultimate:money-wallet-open-bold" class="size-6" />
			</a>
			<hr class="my-5 rounded-full border-2 opacity-15" />
			<a href="/wallets" class="nav-button">
				<Icon icon="material-symbols:wallet" class="m-auto size-6" />
			</a>
		</div>
		<div class="flex flex-col gap-4">
			<a href="/account/settings/" class="nav-button">
				<Icon icon={ICONS_NAMES.accountSettings} class="m-auto size-6" />
			</a>
			<a href="/logout" class="nav-button nav-red">
				<Icon icon="material-symbols:logout-rounded" class="m-auto size-6" />
			</a>
			<div class="text-md text-center text-sm opacity-50">
				<p class="text-center italic">
					v{version}
				</p>
			</div>
		</div>
	</nav>

	<main class="flex-1 px-10 py-6">
		{@render children()}
	</main>

	<Toast {toastStore} />
</div>

<style lang="postcss">
	@reference "../../app.css";

	.nav-button {
		@apply rounded-xl border-2 border-primary-0/15 p-4 text-primary-0 duration-200;
	}

	.nav-button:hover {
		@apply border-primary-0 bg-primary-0 text-primary-1000;
	}

	.nav-button.nav-red {
		@apply border-red-600/50 text-red-600;
	}

	.nav-button.nav-red:hover {
		@apply text-primary-1000 hover:bg-red-600;
	}
</style>
