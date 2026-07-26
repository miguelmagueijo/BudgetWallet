<script lang="ts">
	import Icon from "@iconify/svelte";
	import { onMount } from "svelte";

	let data = $state({});

	onMount(async () => {
		fetch("/api/wallets/", {
			method: "GET",
		});
	});
</script>

<section>
	<a href="/home" class="mb-4 flex w-fit items-center gap-2 underline opacity-50">
		<Icon icon="pajamas:go-back" />
		<span>Home</span>
	</a>
	<h1 class="text-5xl font-bold">My wallets</h1>
</section>
