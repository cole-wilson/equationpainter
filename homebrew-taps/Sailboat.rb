# Created with sailboat, the Python releaser

# v0.24.12

class Sailboat < Formula
  include Language::Python::Virtualenv

  desc "A quick and easy way to distribute your Python projects!"
  homepage "https://github.com/cole-wilson/sailboat"
  url "https://files.pythonhosted.org/packages/18/23/141347532d55f6f30060aaab94b8b5a97fdbb23d5cf410636c160f397710/sailboat-0.24.12.tar.gz" # These lines must be configured during release, not build.
  sha256 "19a9f38047e4af1f4c772faf06d2a8036deb1d0630d5837951f7eae6dd6afef8" # ^^^
  license "MIT"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"

   resource "toml" do
      url "https://files.pythonhosted.org/packages/be/ba/1f744cdc819428fc6b5084ec34d9b30660f6f9daaf70eead706e3203ec3c/toml-0.10.2.tar.gz"
      sha256 "b3bda1d108d5dd99f4a20d24d9c348e91c4db7ab1b749200bded2f839ccbe68f"
   end
   resource "semver" do
      url "https://files.pythonhosted.org/packages/31/a9/b61190916030ee9af83de342e101f192bbb436c59be20a4cb0cdb7256ece/semver-2.13.0.tar.gz"
      sha256 "fa0fe2722ee1c3f57eac478820c3a5ae2f624af8264cbdf9000c980ff7f75e3f"
   end
   resource "requests" do
      url "https://files.pythonhosted.org/packages/6b/47/c14abc08432ab22dc18b9892252efaf005ab44066de871e72a38d6af464b/requests-2.25.1.tar.gz"
      sha256 "27973dd4a904a4f13b263a19c866c13b92a39ed1c964655f025f3f8d3d75b804"
   end
   resource "setuptools" do
      url "https://files.pythonhosted.org/packages/12/68/95515eaff788370246dac534830ea9ccb0758e921ac9e9041996026ecaf2/setuptools-53.0.0.tar.gz"
      sha256 "1b18ef17d74ba97ac9c0e4b4265f123f07a8ae85d9cd093949fa056d3eeeead5"
   end
   resource "twine" do
      url "https://files.pythonhosted.org/packages/f9/43/51c3139667e90399a4d7886013631ad020ad102db5c2907cb240ce56f3c1/twine-3.3.0.tar.gz"
      sha256 "fcffa8fc37e8083a5be0728371f299598870ee1eccc94e9a25cef7b1dcfa8297"
   end


  def install
    virtualenv_install_with_resources
  end
end