# Created with sailboat, the Python releaser

# v3.3.65

class EquationPainter < Formula
  include Language::Python::Virtualenv

  desc "A way for teachers to make equation painter worksheets for their students."
  homepage "https://github.com/cole-wilson/wsm"
  url "{pyhosted}" # These lines must be configured during release, not build.
  sha256 "{sha256}" # ^^^
  license "MIT"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"

   resource "requests" do
      url "https://files.pythonhosted.org/packages/6b/47/c14abc08432ab22dc18b9892252efaf005ab44066de871e72a38d6af464b/requests-2.25.1.tar.gz"
      sha256 "27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804"
   end
   resource "pillow" do
      url "https://files.pythonhosted.org/packages/8f/89/2cf37b88b811f8ac9e7ca79046c976f84098b291e1c05902c09a5ec9e528/Pillow-8.1.0-cp36-cp36m-manylinux1_i686.whl"
      sha256 "93a473b53cc6e0b3ce6bf51b1b95b7b1e7e6084be3a07e40f79b42e83503fbf2"
   end
   resource "xlsxwriter" do
      url "https://files.pythonhosted.org/packages/d9/91/92d6032b2cc80674bacd8cc5c7496a6793df542ad8df0fb8b5acd55b866d/XlsxWriter-1.3.7.tar.gz"
      sha256 "9b1ade2d1ba5d9b40a6d1de1d55ded4394ab8002718092ae80a08532c2add2e6"
   end
   resource "Image" do
      url "https://files.pythonhosted.org/packages/84/be/961693ed384aa91bcc07525c90e3a34bc06c75f131655dfe21310234c933/image-1.5.33.tar.gz"
      sha256 "baa2e09178277daa50f22fd6d1d51ec78f19c12688921cb9ab5808743f097126"
   end
   resource "eel" do
      url "https://files.pythonhosted.org/packages/b3/c2/7dc22cc9ea23f0339316d6d249392d3ce67190430f2b05a316f3471ae15d/Eel-0.14.0.tar.gz"
      sha256 "b21f88c21e050eb2b5f6296f1eeeaf57ad9a2dfbffdf1bf88b90ef05a6ffcdb9"
   end
   resource "gevent" do
      url "https://files.pythonhosted.org/packages/8c/40/913ca6edea1efac2fefd3e51c30c530da12f7d043f7e64cecdde8774571c/gevent-21.1.2-cp27-cp27m-manylinux2010_x86_64.whl"
      sha256 "3694f393ab08372bd337b9bc8eebef3ccab3c1623ef94536762a1eee68821449"
   end
   resource "bottle" do
      url "https://files.pythonhosted.org/packages/ea/80/3d2dca1562ffa1929017c74635b4cb3645a352588de89e90d0bb53af3317/bottle-0.12.19.tar.gz"
      sha256 "a9d73ffcbc6a1345ca2d7949638db46349f5b2b77dac65d6494d45c23628da2c"
   end
   resource "bottle_websocket" do
      url "https://files.pythonhosted.org/packages/17/8e/a22666b4bb0a6e31de579504077df2b1c2f1438136777c728e6cfabef295/bottle-websocket-0.2.9.tar.gz"
      sha256 "9887f70dc0c7592ed8d0d11a14aa95dede6cd08d50d83d5b81fd963e5fec738b"
   end


  def install
    virtualenv_install_with_resources
  end
end