<script>
    import { siteConfig } from "$lib/config";
    import { User } from "lucide-svelte";
</script>

<header>
    <nav class="flex px-4 bg-gray-600 py-3 items-center justify-between">
        <a class="text-white font-bold text-lg" href="/">
            {siteConfig.name}
        </a>
        <a href="/login" class="text-white rounded-full hover:bg-gray-500 p-2">
            <User/>
        </a>
    </nav>
</header>