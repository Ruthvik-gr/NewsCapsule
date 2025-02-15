import LampDemo from "@/components/ui/lamp"

export default function Home() {
  return (
    <div>
      <LampDemo firstword="Read News" words={["Smarter", "Better", "Faster"]} lastwords="Way" />
    </div>
  )
}
