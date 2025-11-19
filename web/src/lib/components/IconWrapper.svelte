<script lang="ts">
	import Icon, { iconLoaded, loadIcons, type IconifyIconLoaderAbort } from "@iconify/svelte";
	import { onDestroy, type Snippet } from "svelte";

	let { icon = $bindable(), classes, fallback }: { icon: string; classes: string; fallback: Snippet } = $props();

	let loaded = $state(false);
	let cleanup: IconifyIconLoaderAbort | null = null;
	let update = $state(0);

	$effect(() => {
		// eslint-disable-next-line @typescript-eslint/no-unused-expressions
		update;

		loaded = iconLoaded(icon);

		if (cleanup) {
			cleanup();
			cleanup = null;
		}

		if (!loaded) {
			cleanup = loadIcons([icon], () => {
				update++;
			});
		}
	});

	onDestroy(() => {
		if (cleanup) {
			cleanup();
		}
	});
</script>

{#if loaded}
	<Icon {icon} class={classes} />
{:else}
	{@render fallback?.()}
{/if}
