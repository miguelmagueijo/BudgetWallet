<script>
	import Icon from "@iconify/svelte";
</script>

<div class="flex h-screen items-center justify-center">
	<div>
		<div class="flex items-center gap-4">
			<Icon
				class="size-14 text-[#30EB72]"
				icon="streamline-ultimate:money-wallet-open-bold"
			/>
			<h1 class="text-center text-6xl font-bold text-[#30EB72]">Budget Wallet</h1>
		</div>
		<div class="mx-auto mt-12 rounded-lg border-2 border-[#1C3023] bg-[#0a1c11] p-14">
			<h2 class="text-center text-4xl font-bold">Login</h2>
			<form class="mt-6">
				<div>
					<label for="lf_username">Username</label>
					<input id="lf_username" type="text" required />
				</div>
				<div class="mt-4">
					<label for="lf_password">Password</label>
					<input id="lf_password" type="password" required />
				</div>
				<button
					type="submit"
					class="mt-8 flex w-full cursor-pointer items-center justify-between rounded-lg bg-[#1D8943] p-3 font-bold duration-300 hover:bg-[#19a64a]"
				>
					<span> Sign in </span>
					<Icon icon="mingcute:arrow-right-fill" class="size-6" />
				</button>
			</form>
		</div>
		<div class="mt-8 opacity-50">
			<p class="text-center">
				Developed by
				<a
					href="https://miguelmagueijo.pt"
					target="_blank"
					class="font-bold underline duration-150 hover:text-[#30EB72]"
				>
					Miguel Magueijo
				</a>
			</p>
			<div class="mt-2 flex items-center justify-center">
				<a
					href="https://github.com/miguelmagueijo/BudgetWallet"
					target="_blank"
					class="duration-150 hover:scale-125 hover:text-[#30EB72]"
				>
					<Icon icon="mingcute:github-fill" class="size-6" />
				</a>
			</div>
		</div>
	</div>
</div>

<style lang="postcss">
	@reference "tailwindcss";

	label {
		@apply font-semibold;
		display: block;
		width: 100%;
	}

	input {
		@apply rounded-lg border-2 border-[#1C3023] bg-[#060D09];
		width: 100%;
	}
</style>
