<script lang="ts">
	import '../app.css';
    import Navbar from './Navbar.svelte';
	let { children } = $props();
</script>

<Navbar/>
<div class="grid grid-cols-12">
	<section class="col-span-2 border-r min-h-screen border-gray-200 pt-3">
		<ul class="flex flex-row">
			<li>
				<a href="#">Dashboard</a>
			</li>
			<li>
				<a href="#">Budget Planner</a>
			</li>			
			<li>
				<a href="#">Projects</a>
			</li>			<li>
				<a href="#">Contributions</a>
			</li>			<li>
				<a href="#">Expenses</a>
			</li>			<li>
				<a href="#">Voting</a>
			</li>
			</li>			<li>
				<a href="#">Reports</a>
			</li>
			<li>
				<a href="#">Community Settings</a>
			</li>
		</ul>
	</section>
	<main class="col-span-10 pt-3 pl-3">
		<h2 class="font-bold">Community Dashboard</h2>
	</main>
</div>
{@render children()}