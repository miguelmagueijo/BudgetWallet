<script lang="ts">
	import { page } from "$app/state";
	import { resolve } from "$app/paths";
</script>

<section class="mt-10 flex flex-col items-center">
	<h1 class="text-6xl font-bold">
		{page.status}
	</h1>
	<h2 class="mt-4 text-4xl font-semibold">
		{page.error ? page.error.message : "Something went wrong!"}
	</h2>
	<a class="primary-button-outline mt-8 w-32 py-2 text-center text-xl" href={resolve("/home")}>Home</a>
</section>
