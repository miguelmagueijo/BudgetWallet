import type { GenericError } from "$lib/types";
import { error } from "@sveltejs/kit";

interface WalletData {
	id: number;
	name: string;
	description: string | null;
	iconify_name: string;
	wallet_total: number;
	color: string;
}

export async function load({ params, fetch }) {
	const walletRes = await fetch(`/api/wallets/${params.walletId}`);

	if (!walletRes.ok) {
		const errorData: GenericError = await walletRes.json();
		console.log(errorData);

		return error(404, errorData.detail);
	}

	const wallet: WalletData = await walletRes.json();

	if (!wallet.color) {
		wallet.color = "#FFFFFF";
	}

	return {
		wallet,
	};
}
