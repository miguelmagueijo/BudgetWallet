<script lang="ts">
	import Icon from "@iconify/svelte";
	import type { PageProps } from "./$types";
	import * as z from "zod";
	import { USERNAME_REGEX, PASSWORD_REGEX } from "$lib/forms.svelte";
	import { invalidateAll } from "$app/navigation";
	import RequirementsOfField from "$lib/components/forms/RequirementsOfField.svelte";
	import { ICONS_NAMES } from "$lib";
	import { getContext } from "svelte";
	import { TOAST_TYPE, type ToastStore } from "$lib/toast.svelte";

	const { data }: PageProps = $props();
	const toastStore = getContext("toastStore") as ToastStore;

	let newUsername: string = $state(data.user.username);
	let canUpdateUsername = $state(true);

	let currPasswordValue = $state("");
	let newPasswordValue = $state("");
	let confNewPasswordValue = $state("");
	const PasswordValidator = z
		.object({
			currPassword: z.string().regex(PASSWORD_REGEX, "Current password doesn't match security requirements"),
			newPassword: z.string().regex(PASSWORD_REGEX, "New password doesn't match security requirements"),
			newConfPassword: z.string(),
		})
		.refine((data) => data.newPassword === data.newConfPassword, { message: "Passwords must match", path: ["newConfPassword"] });

	async function handleUsernameUpdateForm(evt: SubmitEvent) {
		evt.preventDefault();

		if (!newUsername) {
			toastStore.push({
				type: TOAST_TYPE.ERROR,
				message: "Please insert a username",
			});
			return;
		}

		if (!USERNAME_REGEX.test(newUsername)) {
			toastStore.push({
				type: TOAST_TYPE.ERROR,
				message: "New username doesn't meet the requirements",
			});
			return;
		}

		try {
			const formData = new FormData();
			formData.set("username", newUsername);

			const res = await fetch("/api/user/", {
				method: "PATCH",
				body: formData,
			});

			if (!res.ok) {
				const errorData = await res.json();
				toastStore.push({
					message: errorData.detail,
					type: TOAST_TYPE.ERROR,
					duration: 5,
				});
				return;
			}

			canUpdateUsername = false;

			setTimeout(() => {
				canUpdateUsername = true;
			}, 2500);

			toastStore.push({
				message: "Username updated successfully",
				type: TOAST_TYPE.SUCCESS,
				duration: 5,
			});

			invalidateAll();
		} catch (e) {
			toastStore.pushServerError();
			console.error(e);
		}
	}

	async function handlePasswordUpdateForm(evt: SubmitEvent) {
		evt.preventDefault();

		const pwValidation = PasswordValidator.safeParse({
			currPassword: currPasswordValue,
			newPassword: newPasswordValue,
			newConfPassword: confNewPasswordValue,
		});

		if (!pwValidation.success) {
			for (const iss of pwValidation.error.issues) {
				toastStore.push({
					type: TOAST_TYPE.ERROR,
					message: iss.message,
				});
			}
			return;
		}

		if (currPasswordValue === newPasswordValue) {
			toastStore.push({
				type: TOAST_TYPE.ERROR,
				message: "New password is equal to the current one",
			});
			return;
		}

		try {
			const formData = new FormData();
			formData.set("password", currPasswordValue);
			formData.set("newPassword", newPasswordValue);

			const res = await fetch("/api/user/", {
				method: "PATCH",
				body: formData,
			});

			if (!res.ok) {
				const errorData = await res.json();
				toastStore.push({
					message: errorData.detail,
					type: TOAST_TYPE.ERROR,
					duration: 5,
				});
				return;
			}

			toastStore.push({
				message: "Password updated successfully",
				type: TOAST_TYPE.SUCCESS,
				duration: 5,
			});

			currPasswordValue = newPasswordValue = confNewPasswordValue = "";
		} catch (e) {
			toastStore.pushServerError();
			console.error(e);
		}
	}
</script>

<svelte:head>
	<title>BW | Account settings</title>
</svelte:head>

<section class="mx-auto my-10 w-180">
	<div class="flex items-center gap-4">
		<Icon icon={ICONS_NAMES.accountSettings} class="size-10" />
		<h1 class="text-4xl font-bold">Account settings</h1>
		<hr class="flex-1 rounded-lg border-2" />
	</div>
	<div class="mt-6">
		<h2 class="mb-4 text-2xl font-semibold">Change username</h2>
		<form onsubmit={handleUsernameUpdateForm}>
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
			<RequirementsOfField
				requirements={["Start with a letter (A-Z)", "Contain only letters, numbers and underscores (_)", "Length between 3 and 8"]}
			/>
			<button
				type="submit"
				class="primary-button mt-4 w-full py-1"
				disabled={newUsername === data.user.username || !newUsername.length || !canUpdateUsername}
			>
				Update username
			</button>
		</form>
		<hr class="my-6 rounded-lg border-2 border-white opacity-15" />
		<h2 class="mb-4 text-2xl font-semibold">Change password</h2>
		<form onsubmit={handlePasswordUpdateForm}>
			<div>
				<label for="act-curr-pw" class="block">Current password</label>
				<input
					id="act-curr-pw"
					name="currentPassword"
					type="password"
					class=" w-full rounded-lg border-2 border-primary-800 bg-black"
					bind:value={currPasswordValue}
				/>
			</div>
			<RequirementsOfField
				requirements={[
					"Minimum length of 8",
					"One or more letter(s) uppercase",
					"One or more letter(s) lowercase",
					"One or more number(s)",
					"One or more special character(s)",
				]}
			/>
			<div class="mt-3">
				<label for="act-new-pw" class="block">New password</label>
				<input
					id="act-new-pw"
					name="newPassword"
					type="password"
					class=" w-full rounded-lg border-2 border-primary-800 bg-black"
					bind:value={newPasswordValue}
				/>
			</div>
			<RequirementsOfField
				requirements={[
					"Minimum length of 8",
					"One or more letter(s) uppercase",
					"One or more letter(s) lowercase",
					"One or more number(s)",
					"One or more special character(s)",
				]}
			/>
			<div class="mt-3">
				<label for="act-new-pw-confirm" class="block">New password confirmation</label>
				<input
					id="act-new-pw-confirm"
					name="newPasswordConfirm"
					type="password"
					class="w-full rounded-lg border-2 border-primary-800 bg-black"
					bind:value={confNewPasswordValue}
				/>
			</div>
			<RequirementsOfField requirements={["Match previous password field"]} />
			<button type="submit" class="primary-button mt-5 w-full py-1" disabled={!currPasswordValue || !newPasswordValue || !confNewPasswordValue}>
				Update password
			</button>
		</form>
	</div>
</section>
