import { type Handle, redirect } from "@sveltejs/kit";

export const handle: Handle = async ({ event, resolve }) => {
	const token = event.cookies.get("bw_token");

	if (!token && !event.url.pathname.startsWith("/login")) {
		throw redirect(303, "/login");
	}

	if (token) {
		if (event.url.pathname.startsWith("/login")) {
			throw redirect(303, "/home");
		} else if (event.url.pathname.startsWith("/logout")) {
			event.cookies.delete("bw_token", { path: "/" });
			throw redirect(303, "/login");
		}
	}

	return resolve(event);
};
