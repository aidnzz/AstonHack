import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, data }) => {
    const response = await fetch("/vote");
    const votes = await response.json();
    return { votes }
};