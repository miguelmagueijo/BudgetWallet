<script lang="ts">
	import Icon from "@iconify/svelte";
	import { type ToastStore } from "$lib/toast.svelte";

	interface Props {
		toastStore: ToastStore;
	}

	let { toastStore = $bindable() }: Props = $props();
</script>

<div class="toast-container">
	{#each toastStore.activeToasts.values() as toast (toast._jobId)}
		<div class="toast {toast.type.cssClass}">
			<div class="min-w-8">
				<Icon icon={toast.type.icon} class="size-8" />
			</div>
			<p class="toast-text">{toast.message}</p>
			<div class="toast-progress" style="animation-duration: {toast.duration}s"></div>
		</div>
	{/each}
</div>

<style lang="postcss">
	@reference "tailwindcss";

	.toast-container {
		@apply gap-y-4 p-6;
		position: fixed;
		display: grid;
		bottom: 0;
		right: 0;
		z-index: 100;
		background-color: transparent;
	}

	.toast {
		@apply w-80 max-w-80 gap-4 rounded-lg bg-red-200 p-4 font-bold text-red-950 select-none;
		position: relative;
		align-items: center;
		display: flex;
		cursor: pointer;
	}

	.toast.success {
		@apply bg-green-200 text-green-950;
	}

	.toast.error {
		@apply bg-red-200 text-red-950;
	}

	.toast.warning {
		@apply bg-yellow-200 text-yellow-950;
	}

	.toast.info {
		@apply bg-blue-200 text-blue-950;
	}

	.toast-text {
		z-index: 10;
	}

	.toast-progress {
		position: absolute;
		animation: toast-progress-bar linear;
		background-color: black;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		opacity: 15%;
		z-index: 5;
		transform: rotate(180deg);
	}

	@keyframes toast-progress-bar {
		from {
			width: 0;
		}
		to {
			width: 100%;
		}
	}
</style>
