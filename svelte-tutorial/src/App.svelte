<script>
	import Header from './components/header.svelte'
	import Footer from './components/footer.svelte'
	import PollList from './components/pollList.svelte'
	import CreatePollForm from './components/createPollForm.svelte'
	import Tabs from './shared/tabs.svelte'

	//tabs
	let items = ["Current Polls", "Add New Poll"];
	let activeItem = "Current Polls";
	const tabChange = (e) => {
		activeItem = e.detail;
	}

	const handleAdd = (e) => {
		activeItem = "Current Polls";
	}


</script>



<Header />
<main>
	<Tabs {activeItem} {items} on:tabChange={tabChange}/>
	{#if activeItem === "Current Polls"}
		<PollList/>
	{:else if activeItem === "Add New Poll"}
		<CreatePollForm on:add={handleAdd}/>
	{/if}
</main>
<Footer />


<style>
	main {
		max-width: 960px;
		margin: 40px auto;
	}
</style>
