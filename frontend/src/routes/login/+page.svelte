<script>    
</script>


<div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <h2 class="mt-5 text-center text-4xl font-semibold text-black">Sign In</h2>
    </div>
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6" method="POST">
            <div>
                <label for="username" class="block text-sm font-medium text-gray-900">Username</label>
                <div class="mt-2">  
                    <input id="username" name="username" type="text" class="border-0 py-4 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset px-3 sm:text-sm w-full" autocomplete="current-username" required/>
                </div>
            </div>
  
            <div>
                <div class="flex items-center justify-between">
                    <label for="password" class="block text-sm font-medium text-gray-900">Password</label>
                </div>
                <div class="mt-2">
                    <input id="password" name="password" type="password" class="border-0 py-4 text-gray-900 ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset px-3 sm:text-sm w-full" autocomplete="current-password" required/>
                </div>
            </div>
            <button type="submit" class="flex w-full disabled:cursor-not-allowed justify-center bg-gray-400 px-3 py-4 text-sm font-semibold text-white shadow-sm hover:bg-gray-500 focus-visible:outline disabled:opacity-50 focus-visible:outline-offset-2 focus-visible:bg-opacity-90">Sign In</button>
        </form>
  
        <p class="mt-10 text-center text-sm text-gray-500">
            Need an account?
            <a href="/account/create" class="font-semibold leading-6 hover:text-opacity-50">Sign Up</a>
        </p>
    </div>
  </div>