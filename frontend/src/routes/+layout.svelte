<script lang="ts">
	import '../app.css';
    import Navbar from './Navbar.svelte';
	let { children } = $props();
</script>
<svelte:head>
	<title>CFMA</title>
</svelte:head>
<Navbar/>
{@render children()}