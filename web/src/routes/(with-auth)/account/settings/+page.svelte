<script lang="ts">
	import Icon from "@iconify/svelte";
	import type { PageProps } from "./$types";
	import Modal from "$lib/components/Modal.svelte";
	import * as z from "zod";
	import { USERNAME_REGEX } from "$lib";

	const { data }: PageProps = $props();

	let showDeleteAccountModal: boolean = $state(false);

	const PasswordValidator = z
		.object({
			currPassword: z
				.string()
				.regex(
					/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[.,;:#?!@$€%^&+*_|/\\<>-]).{8,}$/,
					"Current password doesn't match security requirements",
				),
			newPassword: z
				.string()
				.regex(
					/^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[.,;:#?!@$€%^&+*_|/\\<>-]).{8,}$/,
					"New password doesn't match security requirements",
				),
			newConfPassword: z.string(),
		})
		.refine((data) => data.newPassword === data.newConfPassword, { message: "Passwords must match", path: ["newConfPassword"] });

	let currPasswordValue = $state("");
	let newPasswordValue = $state("");
	let currConfPasswordValue = $state("");
	let newUsername = $state(data.user.username);

	function handlePasswordUpdateForm() {
		const pwValidation = PasswordValidator.safeParse({
			currentPassword: currPasswordValue,
			newPassword: newPasswordValue,
			newConfPassword: currConfPasswordValue,
		});

		if (!pwValidation.success) {
			console.log(pwValidation.error);
		}
	}
</script>

<section class="m-auto w-[750px]">
	<div class="flex items-center gap-4">
		<h1 class="text-4xl font-bold">Account settings</h1>
		<hr class="flex-1 border-2" />
	</div>
	<div class="mt-6">
		<h2 class="mb-4 text-2xl font-semibold">Change username</h2>
		<form method="POST" action="?/changeUsername">
			<div>
				<label for="act-username" class="block">Username</label>
				<input
					id="act-username"
					name="username"
					type="text"
					class=" w-full rounded-lg border-2 border-primary-800 bg-black"
					bind:value={newUsername}
				/>
			</div>
			<small class="opacity-50">Start with a letter, then letters, numbers or underscores, size ranging 3 to 8</small>
			{#if form?.badUsername}
				<div class="rounded-lg text-sm text-red-500">Invalid username "{form.badUsername}", it doesn't meet the requirements.</div>
			{/if}
			{#if form?.errorMsg}
				<div class="rounded-lg text-sm text-red-500">{form.errorMsg}</div>
			{/if}
			{#if form?.usernameUpdated}
				<div class="rounded-lg text-sm text-green-500">Username updated with success.</div>
			{/if}
			<button
				type="submit"
				class="primary-button mt-4 w-full py-1"
				disabled={newUsername === data.user.username || !USERNAME_REGEX.test(newUsername)}
			>
				Update username
			</button>
		</form>
		<hr class="my-6 rounded-lg border-2 border-white opacity-15" />
		<h2 class="mb-4 text-2xl font-semibold">Change password</h2>
		<form method="POST" onsubmit={handlePasswordUpdateForm} use:enhance>
			<div>
				<label for="act-username" class="block">Current password</label>
				<input
					id="act-curr-pw"
					name="currentPassword"
					type="password"
					class=" w-full rounded-lg border-2 border-primary-800 bg-black"
					value={currPasswordValue}
				/>
			</div>
			<div class="mt-3">
				<label for="act-username" class="block">New password</label>
				<input
					id="act-new-pw"
					name="newPassword"
					type="text"
					class=" w-full rounded-lg border-2 border-primary-800 bg-black"
					value={newPasswordValue}
				/>
			</div>
			<div class="mt-3">
				<label for="act-username" class="block">New password confirmation</label>
				<input
					id="act-new-pw-confirm"
					name="newPasswordConfirm"
					type="text"
					class=" w-full rounded-lg border-2 border-primary-800 bg-black"
					value={currConfPasswordValue}
				/>
			</div>
			<button type="submit" class="primary-button mt-5 w-full py-1">Update password</button>
		</form>
	</div>
	<hr class="mt-10 mb-5 rounded-lg border-2 border-white opacity-15" />
	<div>
		<button
			type="button"
			class="flex w-full cursor-pointer items-center justify-center gap-2 rounded-lg border-2 border-red-500 py-1 text-red-500 duration-300 hover:bg-red-500 hover:text-red-950"
			onclick={() => (showDeleteAccountModal = true)}
		>
			<Icon icon="weui:delete-filled" class="size-5" />
			<span class="font-semibold">Delete account</span>
		</button>
		<Modal bind:showModal={showDeleteAccountModal} title="Confirm account deletion">
			<div class="max-w-[600px] font-bold">
				Do you confirm that all your data will be deleted and it will be impossible to recover it after deleting it?
			</div>
			{#snippet footer()}
				<div class="flex justify-end gap-4">
					<button type="button" class="primary-button px-4 py-2"> Delete </button>
					<button class="primary-button-outline px-4 py-2" type="button" onclick={() => (showDeleteAccountModal = false)}> Cancel </button>
				</div>
			{/snippet}
		</Modal>
	</div>
</section>
