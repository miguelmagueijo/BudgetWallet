export class DataStore<T> {
	private filterFunction: ((element: T) => boolean) | null = $state(null);
	private originalData: Array<T> = $state([]);

	public loading: boolean = $state(false);
	public dataOut: Array<T> = $derived.by(() => {
		if (!this.filterFunction) return this.originalData;

		return this.originalData.filter(this.filterFunction);
	});

	public setData(data: Array<T>) {
		this.originalData = data;
	}

	public applyFilter(filterFunction: (element: T) => boolean) {
		this.filterFunction = filterFunction;
	}

	public resetFilter() {
		this.filterFunction = null;
	}
}
