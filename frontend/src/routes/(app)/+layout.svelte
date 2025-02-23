<script lang="ts">
    let { children } = $props();
	import { page } from '$app/state';

	import { DollarSign, BotMessageSquare, Settings, BookOpen, Blocks, Folder, HandHelping, Vote, HandCoins } from 'lucide-svelte';

	const pages = [
		{
			url: "/",
			title: "Dashboard",
			icon: Blocks
		},
		{
			url: "/budget",
			title: "Budget Planner",
			icon: DollarSign
		},
		{
			url: "/projects",
			title: "Projects",
			icon: Folder,
		},
		{
			url: "/contributions",
			title: "Contributions",
			icon: HandHelping,
		},
		{
			url: "/expenses",
			title: "Expenses",
			icon: HandCoins
		},
		{
			url: "/voting",
			title: "Voting",
			icon: Vote,
		},
		{
			url: "/reports",
			title: "Reports",
			icon: BookOpen 
		},
		{

			url: "/chatbot",
			title: "Chat",
			icon: BotMessageSquare 
		},
	];

</script>

<div class="grid grid-cols-12">
    <section class="col-span-2 p-3 border-r-0 min-h-screen bg-gray-50">
        <ul class="flex flex-col gap-y-3">
			{#each pages as p}
            <li>
                <a href={p.url} class={["flex items-center justify-between px-3 py-2 rounded-sm", page.url.pathname == p.url ? "bg-blue-100" : "bg-white"]}>
					{p.title}
					<p.icon class="size-4"/>
				</a>
            </li>
			{/each}        
		</ul>
    </section>
    <main class="col-span-10 p-3">
		{@render children()}
    </main>
</div>