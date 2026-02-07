export interface SessionUserData {
	id: number;
	username: string;
	is_admin: boolean;
}

export async function load({ fetch }) {
	const user: SessionUserData = await (await fetch("/api/me")).json();

	return {
		user,
	};
}
