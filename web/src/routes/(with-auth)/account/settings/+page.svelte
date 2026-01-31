<script lang="ts">
	import Icon from "@iconify/svelte";

	const { data }: PageProps = $props();
</script>

<section class="w-[750px] m-auto">
	<div class="flex items-center gap-4">
		<h1 class="text-4xl font-bold">Account settings</h1>
		<hr class="border-2 flex-1"/>
	</div>
	<div class="mt-6">
		<h2 class="text-2xl font-semibold">Change your data</h2>
		<form class="mt-4">
			<div>
				<label for="act-username" class="block">
					Username
				</label>
				<input id="act-username" name="username" type="text" class=" w-full bg-black border-2 rounded-lg" value="{data.user.username}"/>
			</div>
		</form>
	</div>
	<div class="mt-6">
		<button type="button" class="text-red-500 flex gap-2 items-center border-2 border-red-500 rounded-lg w-full p-2 justify-center">
			<Icon icon="weui:delete-filled" class="size-8"/>
			<span class="font-semibold">
				Delete account
			</span>
		</button>
	</div>
</section>