# Created with sailboat, the Python releaser

# v1.0.0

class Test_Project < Formula
  include Language::Python::Virtualenv

  desc ""
  homepage "https://github.com/cole-wilson/sail-test"
  url "https://files.pythonhosted.org/packages/c9/c7/ee6997f5d51205bc4834be52a1d215d6912b147a21ad9eccbeefd2fffcfa/sail-test-1.0.0.tar.gz" # These lines must be configured during release, not build.
  sha256 "3f069f4e4e3d974694ec32d9397f0d06e67ef353391694c1597574236dc498df" # ^^^
  license "MIT"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"



  def install
    virtualenv_install_with_resources
  end
end