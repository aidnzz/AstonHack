<script lang="ts">
    import type { PageProps } from './$types';
    let buttonModal = $state(false);

    let { data }: PageProps = $props();
</script>

<h1 class="font-semibold text-3xl text-black">Votes</h1>
<p>Below are the votes for projects.</p>

<section class="min-h-[50vh] w-full">
    {#each data.votes as vote}
        <div>
            {vote}
        </div>
    {:else}
        <div class="max-w-full mt-6 h-4 animate-pulse text-base antialiased font-light leading-relaxed bg-gray-300 rounded-full text-inherit w-72"></div>
    {/each}
</section>

<div class="flex flex-row-reverse">
    <button class="flex disabled:cursor-not-allowed justify-center bg-gray-400 px-3 py-4 text-sm font-semibold text-white shadow-sm hover:bg-gray-500 focus-visible:outline disabled:opacity-50 focus-visible:outline-offset-2 focus-visible:bg-opacity-90 rounded-md">Add Vote</button>
</div>