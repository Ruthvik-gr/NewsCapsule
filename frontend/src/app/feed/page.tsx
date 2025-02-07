"use client"
const Page = () => {
    return (
        <div className='flex items-center justify-center min-h-screen bg-black p-4'>
            <div className='w-full max-w-md bg-white text-black p-6 rounded-2xl shadow-lg overflow-y-auto max-h-screen h-full'>
                <h2 className='text-2xl font-bold mb-4'>Feed Title</h2>
                <p className='text-sm pr-2'>
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec sit amet nunc vehicula, pellentesque erat id, mollis velit. Integer eu felis non arcu aliquam dictum. Nulla facilisi. Sed faucibus dolor non tortor pulvinar, nec tincidunt nulla tristique.
                    <br /><br />
                    Aenean ut lorem non nunc sollicitudin vehicula ac ut turpis. Ut fringilla mauris nec arcu laoreet, sed facilisis mi fringilla. Duis tincidunt, lorem a malesuada tempor, odio justo venenatis sapien, eu interdum nisi libero a purus.
                    <br /><br />
                    Cras nec ligula vel metus malesuada suscipit non sit amet lorem. Vivamus suscipit vestibulum mauris, in ultricies magna facilisis id. Integer nec volutpat libero. Nam fringilla consequat odio, id pharetra purus malesuada et.
                </p>
            </div>
        </div>
    );
};

export default Page;