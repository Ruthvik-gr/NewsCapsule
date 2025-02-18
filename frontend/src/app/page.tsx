import LampDemo from "@/components/ui/lamp"

export default function Home() {
  return (
    <div>
      <LampDemo firstword="Read News" words={["Smarter", "Better", "Faster"]} lastwords="Way" />
      <p className="absolute bottom-10 left-0 right-0 text-center text-sm md:text-white mt-4">
        Developed with ❤️ by{" "}
        <a
          href="https://ruthvikghagarwaleportfolio.netlify.app/"
          className="text-[#16c6e2] hover:underline"
          target="_blank"
          rel="noopener noreferrer"
        >
          Ruthvik Ghagarwale
        </a>
      </p>

    </div>
  )
}
