import { SvelteMap } from "svelte/reactivity";
import { ICONS_NAMES } from "$lib/index";

export const TOAST_TYPE = {
	SUCCESS: {
		cssClass: "success",
		icon: ICONS_NAMES.roundCheck,
	},
	ERROR: {
		cssClass: "error",
		icon: ICONS_NAMES.roundError,
	},
	INFO: {
		cssClass: "info",
		icon: ICONS_NAMES.roundInfo,
	},
	WARNING: {
		cssClass: "warning",
		icon: ICONS_NAMES.roundWarning,
	},
} as const;

export interface ToastInfo {
	/** Internal, do not set this */
	_jobId?: number;
	/** Type of the toast */
	type: (typeof TOAST_TYPE)[keyof typeof TOAST_TYPE];
	/** Message shown to the user */
	message: string;
	/** Duration in seconds */
	duration?: number;
}

export class ToastStore {
	public activeToasts: Map<number, ToastInfo> = new SvelteMap();

	public push(toastInfo: ToastInfo) {
		if (typeof toastInfo.duration !== "number") {
			toastInfo.duration = 5;
		}

		const jobID = window.setTimeout(() => {
			this.activeToasts.delete(jobID);
		}, toastInfo.duration * 1000);

		toastInfo._jobId = jobID;

		this.activeToasts.set(jobID, toastInfo);
	}

	public pushServerError() {
		this.push({
			message: "Something went wrong!",
			type: TOAST_TYPE.ERROR,
			duration: 5,
		});
	}

	public deleteToast(targetId: number | undefined) {
		if (typeof targetId !== "number") {
			return;
		}

		this.activeToasts.delete(targetId);
	}
}
