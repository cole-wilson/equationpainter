# Created with sailboat, the Python releaser

# v0.0.1+43c3eda.2

class empty_project < Formula
  include Language::Python::Virtualenv

  desc "empty project for sailboat testing"
  homepage "https://github.com/cole-wilson/empty"
  url "https://files.pythonhosted.org/packages/a4/d4/8ec24ca59be0b85be04c57cc36489c6c17c710c3f631fd5ab42551c68768/emptyproject1-0.0.1.tar.gz" # These lines must be configured during release, not build.
  sha256 "0c9f2da03ef325aa733e4e006f26883bf62c9587a550041802a13a68e446be48" # ^^^
  license "none"

  livecheck do
    url :stable
  end

  depends_on "python@3.9"



  def install
    virtualenv_install_with_resources
  end
end