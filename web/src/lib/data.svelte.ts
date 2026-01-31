export class DataStore<T> {
	private filterFunction: ((element: T) => boolean) | null = $state(null);
	private sortFunction: ((a: T, b: T) => number) | null = $state(null);
	private originalData: Array<T> = $state([]);

	public loading: boolean = $state(false);
	public dataOut: Array<T> = $derived.by(() => {
		let output = this.originalData.slice();

		if (output.length === 0) {
			return output;
		}

		if (this.filterFunction) {
			output = output.filter(this.filterFunction);
		}

		if (this.sortFunction) {
			output = output.sort(this.sortFunction);
		}

		return output;
	});

	public setData(data: Array<T>) {
		this.originalData = data;
	}

	public addRecord(record: T) {
		this.originalData.push(record);
	}

	public isEmpty() {
		return this.originalData.length === 0;
	}

	public getSize() {
		return this.originalData.length;
	}

	public isOutEmpty() {
		return this.dataOut.length === 0;
	}

	public applySort(sortFunction: (a: T, b: T) => number) {
		this.sortFunction = sortFunction;
	}

	public resetSort() {
		this.sortFunction = null;
	}

	public applyFilter(filterFunction: (element: T) => boolean) {
		this.filterFunction = filterFunction;
	}

	public resetFilter() {
		this.filterFunction = null;
	}
}
