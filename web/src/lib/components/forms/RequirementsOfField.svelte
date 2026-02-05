<script lang="ts">
	import Icon from "@iconify/svelte";
	import { ICONS_NAMES } from "$lib";

	interface Props {
		requirements: Array<string>;
	}

	const { requirements }: Props = $props();
</script>

<div class="group relative mt-1 cursor-help">
	<div class="flex items-center gap-1 opacity-50 select-none">
		<p class="text-sm">Requirements</p>
		<Icon icon={ICONS_NAMES.roundInfo} class="size-4" />
	</div>
	<div class="absolute top-full left-0 z-10 hidden rounded-lg border-2 border-gray-600 bg-black p-2 text-sm select-none group-hover:block">
		<p class="text-xs opacity-50">Field requirements</p>
		{#if requirements.length === 1}
			<p>{requirements[0]}</p>
		{:else}
			<ul class="list-inside list-disc text-gray-200">
				{#each requirements as req, idx (idx)}
					<li>{req}</li>
				{/each}
			</ul>
		{/if}
	</div>
</div>
