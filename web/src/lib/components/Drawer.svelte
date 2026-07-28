<script lang="ts">
	import type { Snippet } from "svelte";

	interface Props {
		showDrawer: boolean;
		closeCallback?: () => void;
		openCallback?: () => void;
		children: Snippet;
		header?: Snippet;
		footer?: Snippet;
	}

	let { showDrawer = $bindable(), closeCallback, openCallback, header, footer, children }: Props = $props();

	$effect(() => {
		if (showDrawer) {
			if (openCallback) openCallback();
		} else {
			if (closeCallback) closeCallback();
		}
	});
</script>

<div class="fixed inset-0 top-0 right-0 bottom-0 left-0 z-50 duration-200" class:opacity-0={!showDrawer} class:invisible={!showDrawer}>
	<div class="flex">
		<button onclick={() => (showDrawer = false)} title="" class="block h-screen flex-1 bg-black/75"></button>
		<div
			class="absolute top-0 right-0 bottom-0 flex min-w-1/2 flex-col bg-primary-950 transition-all duration-200"
			class:translate-x-full={!showDrawer}
			class:translate-x-0={showDrawer}
		>
			{#if header !== undefined}
				<div class="w-full bg-primary-1000 p-6">
					{@render header()}
				</div>
			{/if}
			<div class="p-6">
				{@render children()}
			</div>
			{#if footer !== undefined}
				<div class="flex flex-1 items-end justify-start">
					<div class="w-full bg-primary-1000 p-6">
						{@render footer()}
					</div>
				</div>
			{/if}
		</div>
	</div>
</div>
