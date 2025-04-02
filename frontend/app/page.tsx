import Image from "next/image";
import "@radix-ui/themes/styles.css";
import { Theme} from "@radix-ui/themes";
import SearchBar from "@/components/textarea";


export default function Page() {
  return(
    <Home/>
  );
}

function Home() {
  return (
      <div className="w-100% h-100%">
        <Theme accentColor="brown" grayColor="sand" radius="full">
          <header className="flex justify-between items-center p-4 border-b">
              <h1 className="text-xl font-bold">Landing Page Lead Funnel Validation Tool</h1>
          </header>
        <div className="flex flex-col justify-center items-center min-h-[calc(100vh-80px)] w-full max-w-4xl mx-auto">
          <div className="flex flex-col items-center w-full">
            <h1 className="text-5xl font-bold text-center mb-6 w-full max-w-2xl">Input a landing URL</h1>
              <div className="w-full max-w-2xl">
                <SearchBar />
              </div>
          </div>
        </div>
        </Theme>
      </div>
  );
}