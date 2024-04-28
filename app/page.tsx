import Image from "next/image";
import Link from "next/link";
import { NavBar } from "./components/NavBar/NavBar";
import { Camera } from "./components/Camera/Camera";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
        <Camera />
    </main>
  );
}
