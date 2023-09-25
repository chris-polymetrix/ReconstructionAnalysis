import open3d as o3d
import numpy as np
from pathlib import Path
from scipy.spatial.transform import Rotation


def main():
    point_cloud_path = Path("data/frames")
    transforms_path = Path("data/transforms")

    pcs = load_pcs(point_cloud_path)
    transforms = load_transforms(transforms_path)

    print(len(pcs), len(transforms))

    # Need to create an array of target and source data pairs to visualise
    # Need to capture:
    #   1. A set of raw - untransformed point clouds
    #   2. A set of each transform created by the icp process


def visualise_icp(data):
    vis = o3d.visualization.Visualizer()
    vis.create_window()

    # geometry is the point cloud used in your animaiton
    target = o3d.geometry.PointCloud()
    target.paint_uniform_color([1, 0.706, 0])
    vis.add_geometry(target)

    source = o3d.geometry.PointCloud()
    source.paint_uniform_color([0, 0.651, 0.929])
    vis.add_geometry(source)

    for target_data, source_data in data:
        target.points = target_data
        vis.update_geometry(target)
        source.points = source_data
        vis.update_geometry(source)

        vis.poll_events()
        vis.update_renderer()


def load_pcs(path: Path):
    pcs = []
    for pc_path in sorted(path.glob("*.obj")):
        x = np.loadtxt(pc_path, delimiter=",")
        pc = o3d.geometry.PointCloud()
        pc.points = o3d.utility.Vector3dVector(x)
        pcs.append(pc)

    return pcs

def load_transforms(path: Path):
    


    return [np.apply_along_axis(to_transform_matrix, 1, np.loadtxt(t_path, delimiter=",")) for t_path in path.glob("*.csv")]
        


def to_transform_matrix(x):
    rot: Rotation = Rotation.from_euler("ZYX", x[-3:])
    trans = x[:3]

    mat = np.zeros((4,4))
    mat[:3, :3] = rot.as_matrix()
    mat[:3, -1] = trans

    return mat

if __name__ == "__main__":
    main()