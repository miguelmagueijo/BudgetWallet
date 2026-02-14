export const USERNAME_REGEX = /^[a-zA-Z][A-Za-z0-9_]{2,7}$/;
export const BUDGET_NAME_REGEX = /^[a-zA-Z][A-Za-z0-9_ -]{1,30}[A-Za-z0-9_]$/;
export const PASSWORD_REGEX = /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[.,;:#?!@$€%^&+*_|/\\<>-]).{8,}$/;
export const ICONIFY_ICON_REGEX = /^[a-z0-9]+(-[a-z0-9]+)*:[a-z0-9]+(-[a-z0-9]+)*$/;
export const HEX_COLOR_REGEX = /^#(?:[0-9a-fA-F]{3}){1,2}$/;

export class FormErrorHandler {
	private _isError: boolean = $state(false);
	private _message: string | null = $state(null);

	public setError(message: string) {
		this._isError = true;
		this._message = message ?? "Something went wrong, please contact the administrator";
	}

	public setSuccess(message: string) {
		this._isError = false;
		this._message = message;
	}

	get isError(): boolean {
		return this._isError;
	}

	get message(): string | null {
		return this._message;
	}

	public reset() {
		this._message = null;
		this._isError = false;
	}
}
