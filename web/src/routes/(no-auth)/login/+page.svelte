<script lang="ts">
	import Icon from "@iconify/svelte";

	let isLoading: boolean = false;
	let usernameElement: HTMLInputElement;
	let passwordElement: HTMLInputElement;
	let errorMsg: string | null = null;

	async function onLoginSubmit() {
		if (isLoading) {
			return;
		}

		isLoading = true;

		const formData = new FormData();
		formData.append("username", usernameElement.value);
		formData.append("password", passwordElement.value);

		try {
			const res = await fetch("http://localhost:5173/api/login", {
				method: "POST",
				body: formData,
			});

			if (res.ok) {
				window.location.replace("/home");
			} else {
				if (res.status === 400 || res.status === 401) {
						const resData = await res.json();

						errorMsg = resData.detail;
				} else {
					errorMsg = "Something went wrong! Please contact an administrator";
				}
			}
		} catch {
			errorMsg = "Something went wrong! Please contact an administrator";
		}

		isLoading = false;
	}
</script>

<svelte:head>
	<title>Log In into Budget Wallet</title>
</svelte:head>

<div class="flex h-screen items-center justify-center">
	<div>
		<div class="mb-12 flex items-center gap-4 text-primary-400">
			<Icon
				class="size-14"
				icon="streamline-ultimate:money-wallet-open-bold"
			/>
			<h1 class="text-center text-6xl font-bold">Budget Wallet</h1>
		</div>
		{#if errorMsg}
			<div
				class="mb-6 rounded-lg border-2 border-transparent bg-red-200 p-2 text-center font-semibold text-red-800"
			>
				{errorMsg}
			</div>
		{/if}
		<div class="mx-auto rounded-lg border-2 border-primary-900 bg-primary-950 p-14">
			<h2 class="text-center text-4xl font-bold">Login</h2>
			<form class="mt-6" on:submit|preventDefault={onLoginSubmit}>
				<div>
					<label for="lf_username">Username</label>
					<input
						id="lf_username"
						type="text"
						class="border-2 border-primary-900 bg-black w-full rounded-lg"
						required
						class:withErrors={errorMsg}
						bind:this={usernameElement}
					/>
				</div>
				<div class="mt-4">
					<label for="lf_password">Password</label>
					<input
						id="lf_password"
						type="password"
						class="border-2 border-primary-900 bg-black w-full rounded-lg"
						required
						class:withErrors={errorMsg}
						bind:this={passwordElement}
					/>
				</div>
				<button type="submit" class="primary-button w-full flex items-center justify-between py-2 px-4 mt-8" disabled="{isLoading}">
					{#if isLoading}
						<span> Logging you in... </span>
						<Icon icon="gg:spinner" class="size-6 animate-spin" />
					{:else}
						<span> Sign in </span>
						<Icon icon="mingcute:arrow-right-fill" class="size-6" />
					{/if}
				</button>
			</form>
		</div>
		<div class="mt-8 text-center opacity-50">
			To open an account you must contact an administrator
		</div>
		<hr class="mx-auto my-4 w-1/3 rounded-full opacity-25" />
		<div class="opacity-50">
			<p class="text-center">
				Developed by
				<a
					href="https://miguelmagueijo.pt"
					target="_blank"
					class="font-bold underline duration-300 hover:text-primary-400"
				>
					Miguel Magueijo
				</a>
			</p>
			<div class="mt-2 flex items-center justify-center">
				<a
					href="https://github.com/miguelmagueijo/BudgetWallet"
					target="_blank"
					class="duration-300 hover:scale-125 hover:text-primary-400"
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

	input.withErrors {
		@apply border-red-400;
	}
</style>
