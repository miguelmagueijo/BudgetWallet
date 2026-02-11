<script lang="ts">
	import Icon from "@iconify/svelte";
	import type { Snippet } from "svelte";

	interface Props {
		showModal: boolean;
		title: string | undefined;
		footer: Snippet | undefined;
		children: Snippet;
	}

	let { showModal = $bindable(), title, footer = undefined, children }: Props = $props();
	let dialogElement: HTMLDialogElement;

	function handleDialogOnClick(event: Event) {
		if (event.target === dialogElement) {
			showModal = false;
		}
	}

	$effect(() => {
		if (showModal) {
			dialogElement.show();
		} else {
			dialogElement.close();
		}
	});
</script>

<dialog
	class="z-100 bg-black/25 text-primary-50 backdrop-blur-xs"
	closedby="closerequest"
	onclick={handleDialogOnClick}
	onclose={() => (showModal = false)}
	bind:this={dialogElement}
>
	<div class="modal-content-container border-primary-800 bg-primary-1000">
		<div class="flex min-h-full flex-col">
			<div
				class="{title
					? 'items-center'
					: 'items-end'} flex justify-between border-b-2 border-primary-900 bg-primary-800 p-4 text-2xl font-bold"
			>
				{#if title}
					<span>{title}</span>
				{/if}
				<button class="cursor-pointer" type="button" onclick={() => (showModal = false)}>
					<Icon icon="iconamoon:close-bold" class="size-8" />
				</button>
			</div>
			<div class="flex-1 p-4">
				{@render children()}
			</div>
			{#if footer !== undefined}
				<div class="mt-auto p-4">
					{@render footer()}
				</div>
			{/if}
		</div>
	</div>
</dialog>

<style lang="postcss">
	@reference "tailwindcss";

	dialog {
		width: 100vw;
		height: 100vh;
		top: 0;
		left: 0;
	}

	dialog[open] {
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.modal-content-container {
		@apply my-20 rounded-lg border-4;
		min-height: 200px;
		min-width: 500px;
		max-height: 90vh;
		overflow-y: scroll;
	}
</style>
