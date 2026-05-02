import Image from 'next/image';

type AppImageProps = {
  src: string;
  alt: string;
  width: number;
  height: number;
  className?: string;
};

export default function AppImage({ src, alt, width, height, className }: AppImageProps) {
  return <Image src={src} alt={alt} width={width} height={height} className={className} />;
}
