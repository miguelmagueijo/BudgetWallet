<script lang="ts">
	import Icon from "@iconify/svelte";
	import type { Snippet } from "svelte";

	let { showModal = $bindable(), title, children }: { showModal: boolean; title: string | undefined; children: Snippet } = $props();
	let dialogElement: HTMLDialogElement;

	$effect(() => {
		if (showModal) {
			dialogElement.showModal();
		} else {
			dialogElement.close();
		}
	});
</script>

<dialog class="border-primary-800 bg-primary-1000 text-primary-50" closedby="any" onclose={() => (showModal = false)} bind:this={dialogElement}>
	<div class="flex min-h-full flex-col">
		<div class="{title ? 'items-center' : 'items-end'} flex justify-between border-b-2 border-primary-900 bg-black p-4 text-2xl font-bold">
			{#if title}
				<span>{title}</span>
			{/if}
			<button class="cursor-pointer" type="button" onclick={() => dialogElement.close()}>
				<Icon icon="iconamoon:close-bold" class="size-8" />
			</button>
		</div>
		<div class="flex-1 p-4">
			{@render children()}
		</div>
		<div class="mt-auto p-4">Footer</div>
	</div>
</dialog>

<style lang="postcss">
	@reference "tailwindcss";

	dialog {
		@apply rounded-lg border-4;
		left: 50%;
		top: 50%;
		transform: translate(-50%, -50%);
		min-height: 200px;
		min-width: 500px;
	}

	dialog::backdrop {
		background-color: rgba(0, 0, 0, 0.8);
	}
</style>
